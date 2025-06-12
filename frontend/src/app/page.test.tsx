// frontend/src/app/page.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from './page'; // Adjust path if necessary

// Mock the fetch function
global.fetch = jest.fn();

// Mock child components
jest.mock('@/components/ProductCard', () => ({
  ProductCard: ({ product }: { product: any }) => (
    <div data-testid={`product-card-${product.id}`} onClick={() => product.onClick && product.onClick()}>
      {product.description}
    </div>
  ),
}));

// TryOnDisplay mock needs to reflect its new props
jest.mock('@/components/TryOnDisplay', () => ({
  TryOnDisplay: ({ generatedImageSrc, isLoading, error }: { generatedImageSrc: string | null, isLoading: boolean, error: string | null }) => (
    <div data-testid="try-on-display">
      {isLoading && <p>Generating your try-on image with AI...</p>}
      {error && <p>Error: {error}</p>}
      {generatedImageSrc && <img src={generatedImageSrc} alt="Generated Try-On" />}
      {!isLoading && !error && !generatedImageSrc && <p>Select a model and a product, then click "Generate Try-On".</p>}
    </div>
  ),
}));

jest.mock('framer-motion', () => ({
  motion: {
    div: jest.fn(({ children, ...rest }) => <div {...rest}>{children}</div>),
  },
}));

const mockProducts = [
  { id: 'prod1', name: 'Product 1 Alpha Name', description: 'Product 1 Alpha', type: 'dress', image: 'data:image/jpeg;base64,prod1_base64data', price: '$10' },
  { id: 'prod2', name: 'Product 2 Beta Name', description: 'Product 2 Beta', type: 'shirt', image: 'data:image/jpeg;base64,prod2_base64data', price: '$20' },
];

const mockUsers = [
  { id: 'user1', name: 'User Alpha', description: 'Description for User Alpha' },
  { id: 'user2', name: 'User Beta', description: 'Description for User Beta' },
];

const mockUser1Display = { id: 'user1', name: 'User Alpha', description: 'Description for User Alpha', image: 'data:image/jpeg;base64,user1_base64data' };
// Product display data is already fetched initially in page.tsx, so selectedProduct will have its image.

describe('Home Page - AI Try-On Functionality', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockReset();

    // Default mocks for initial data loading (products, users, and their display images)
    (global.fetch as jest.Mock).mockImplementation((url: string) => {
      const urlObj = new URL(url); // Use URL object for easier path checking
      if (urlObj.pathname.endsWith('/products') && !urlObj.pathname.includes('/display')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockProducts) });
      }
      // Match /products/prod1/display, /products/prod2/display etc.
      const productDisplayMatch = urlObj.pathname.match(/^\/products\/(prod\d+)\/display$/);
      if (productDisplayMatch) {
        const productId = productDisplayMatch[1];
        const product = mockProducts.find(p => p.id === productId);
        return Promise.resolve({ ok: true, json: () => Promise.resolve(product) }); // Product itself contains the base64 image
      }
      if (urlObj.pathname.endsWith('/users') && !urlObj.pathname.includes('/display')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockUsers) });
      }
      // Match /users/user1/display etc.
      const userDisplayMatch = urlObj.pathname.match(/^\/users\/(user\d+)\/display$/);
      if (userDisplayMatch) {
         const userId = userDisplayMatch[1];
         if (userId === 'user1') return Promise.resolve({ ok: true, json: () => Promise.resolve(mockUser1Display) });
         // Add other user display mocks if needed for other tests
         const user = mockUsers.find(u => u.id === userId);
         if (user) return Promise.resolve({ ok: true, json: () => Promise.resolve({...user, image: `data:image/jpeg;base64,${userId}_base64data`})});
      }
      // Do not reject unhandled calls by default for the generic setup
      // Let specific tests override for /api/v1/tryon/generate or fail if unexpected calls are made
      console.warn(`Unhandled fetch mock for URL in default setup: ${url}`);
      return Promise.resolve({ ok: false, status: 404, json: () => Promise.resolve({ detail: `Mock not found for ${url}`})});
    });
  });

  test('renders initial state with generate button disabled', async () => {
    render(<Home />);
    await waitFor(() => expect(screen.getByText('Product 1 Alpha')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByText('User Alpha', {selector: 'option'})).toBeInTheDocument()); // User in dropdown

    expect(screen.getByRole('button', { name: /Generate AI Try-On/i })).toBeDisabled();
    // Initial text in TryOnDisplay mock
    expect(screen.getByText('Select a model and a product, then click "Generate Try-On".')).toBeInTheDocument();
  });

  test('generate button becomes enabled after selecting user and product', async () => {
    render(<Home />);
    await waitFor(() => expect(screen.getByText('User Alpha', {selector: 'option'})).toBeInTheDocument());

    // Select user
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'user1' } });
    await waitFor(() => expect(screen.getByText(mockUser1Display.name, { selector: 'h3' })).toBeInTheDocument());

    // Select product (click its parent motion.div)
    const productCard = screen.getByText(mockProducts[0].description);
    fireEvent.click(productCard.parentElement!);
    // Check for selected product name in the "Selected Product (for AI generation)" card
    await waitFor(() => expect(screen.getByText(mockProducts[0].name, { exact: false })).toBeInTheDocument());


    expect(screen.getByRole('button', { name: /Generate AI Try-On/i })).toBeEnabled();
  });

  test('clicking "Generate AI Try-On" shows loading state, then displays generated image on success', async () => {
    (global.fetch as jest.Mock).mockImplementation(async (url: string, options?: RequestInit) => {
        const urlObj = new URL(url, 'http://localhost'); // Base URL needed if only path is passed
        if (urlObj.pathname === '/api/v1/tryon/generate') {
            return Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ generated_image_base64: 'data:image/jpeg;base64,new_generated_image_data', mimetype: 'image/jpeg' }),
            });
        }
        // Fallback to default mocks for initial loads
        if (urlObj.pathname.endsWith('/products') && !urlObj.pathname.includes('/display')) return Promise.resolve({ ok: true, json: () => Promise.resolve(mockProducts) });
        const productDisplayMatch = urlObj.pathname.match(/^\/products\/(prod\d+)\/display$/);
        if (productDisplayMatch) return Promise.resolve({ ok: true, json: () => Promise.resolve(mockProducts.find(p=>p.id === productDisplayMatch[1]))});
        if (urlObj.pathname.endsWith('/users') && !urlObj.pathname.includes('/display')) return Promise.resolve({ ok: true, json: () => Promise.resolve(mockUsers) });
        if (urlObj.pathname.includes('/users/user1/display')) return Promise.resolve({ ok: true, json: () => Promise.resolve(mockUser1Display) });

        console.error(`Unhandled fetch in SUCCESS test: ${url}`);
        return Promise.reject(new Error(`Unhandled fetch in test: ${url}`));
    });

    render(<Home />);
    await waitFor(() => expect(screen.getByText('User Alpha', {selector: 'option'})).toBeInTheDocument());

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'user1' } });
    await waitFor(() => expect(screen.getByText(mockUser1Display.name, { selector: 'h3' })).toBeInTheDocument());

    fireEvent.click(screen.getByText(mockProducts[0].description).parentElement!);
    await waitFor(() => expect(screen.getByText(mockProducts[0].name, { exact: false })).toBeInTheDocument());

    const generateButton = screen.getByRole('button', { name: /Generate AI Try-On/i });
    fireEvent.click(generateButton);

    await waitFor(() => expect(screen.getByText('Generating your try-on image with AI...')).toBeInTheDocument());
    expect(generateButton).toBeDisabled();
    // The button text changes to 'Generating...'
    expect(screen.getByRole('button', { name: /Generating.../i })).toBeInTheDocument();

    await waitFor(() => {
        const tryOnDisplay = screen.getByTestId('try-on-display');
        const generatedImage = tryOnDisplay.querySelector('img[alt="Generated Try-On"]');
        expect(generatedImage).toBeInTheDocument();
        expect(generatedImage).toHaveAttribute('src', 'data:image/jpeg;base64,new_generated_image_data');
    }, { timeout: 3000 });

    expect(generateButton).toBeEnabled(); // Button should be re-enabled
    expect(screen.getByRole('button', { name: /Generate AI Try-On/i })).toBeInTheDocument();
  });

  test('clicking "Generate AI Try-On" shows error state on API failure', async () => {
    const errorMessage = "AI generation failed spectacularly.";
    (global.fetch as jest.Mock).mockImplementation(async (url: string, options?: RequestInit) => {
        const urlObj = new URL(url, 'http://localhost');
        if (urlObj.pathname === ('/api/v1/tryon/generate')) {
            return Promise.resolve({
                ok: false,
                status: 500,
                json: () => Promise.resolve({ detail: errorMessage }),
            });
        }
        // Fallback for initial loads
        if (urlObj.pathname.endsWith('/products') && !urlObj.pathname.includes('/display')) return Promise.resolve({ ok: true, json: () => Promise.resolve(mockProducts) });
        const productDisplayMatch = urlObj.pathname.match(/^\/products\/(prod\d+)\/display$/);
        if (productDisplayMatch) return Promise.resolve({ ok: true, json: () => Promise.resolve(mockProducts.find(p=>p.id === productDisplayMatch[1]))});
        if (urlObj.pathname.endsWith('/users') && !urlObj.pathname.includes('/display')) return Promise.resolve({ ok: true, json: () => Promise.resolve(mockUsers) });
        if (urlObj.pathname.includes('/users/user1/display')) return Promise.resolve({ ok: true, json: () => Promise.resolve(mockUser1Display) });

        console.error(`Unhandled fetch in FAILURE test: ${url}`);
        return Promise.reject(new Error(`Unhandled fetch in test: ${url}`));
    });

    render(<Home />);
    await waitFor(() => expect(screen.getByText('User Alpha', {selector: 'option'})).toBeInTheDocument());

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'user1' } });
    await waitFor(() => expect(screen.getByText(mockUser1Display.name, { selector: 'h3' })).toBeInTheDocument());

    fireEvent.click(screen.getByText(mockProducts[0].description).parentElement!);
    await waitFor(() => expect(screen.getByText(mockProducts[0].name, { exact: false })).toBeInTheDocument());

    const generateButton = screen.getByRole('button', { name: /Generate AI Try-On/i });
    fireEvent.click(generateButton);

    await waitFor(() => expect(screen.getByText('Generating your try-on image with AI...')).toBeInTheDocument());

    await waitFor(() => expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument(), { timeout: 3000 });

    expect(generateButton).toBeEnabled();
    expect(screen.getByRole('button', { name: /Generate AI Try-On/i })).toBeInTheDocument();
  });
});
