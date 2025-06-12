// frontend/src/components/TryOnDisplay.test.tsx
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { TryOnDisplay } from './TryOnDisplay';

describe('TryOnDisplay', () => {
  const generatedImageSrc = 'data:image/jpeg;base64,generatedImageData';

  test('renders loading state when isLoading is true', () => {
    render(<TryOnDisplay generatedImageSrc={null} isLoading={true} error={null} />);
    expect(screen.getByText('Generating your try-on image with AI...')).toBeInTheDocument();
    expect(screen.getByText('This may take a moment.')).toBeInTheDocument();
    // Simple check for the spinner div based on its animation class could be an option
    // but text presence is often more resilient to minor style changes.
    // Example: expect(document.querySelector('.animate-spin')).toBeInTheDocument();
  });

  test('renders error state when error is provided', () => {
    const errorMessage = 'Failed to generate image.';
    render(<TryOnDisplay generatedImageSrc={null} isLoading={false} error={errorMessage} />);
    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
  });

  test('renders placeholder when no image, not loading, and no error', () => {
    render(<TryOnDisplay generatedImageSrc={null} isLoading={false} error={null} />);
    expect(screen.getByText('Select a model and a product, then click "Generate Try-On".')).toBeInTheDocument();
  });

  test('renders generated image when src is provided and not loading/error', () => {
    render(<TryOnDisplay generatedImageSrc={generatedImageSrc} isLoading={false} error={null} />);
    const img = screen.getByAltText('Generated Try-On');
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('src', generatedImageSrc);
  });

  test('loading state takes precedence over image src', () => {
    render(<TryOnDisplay generatedImageSrc={generatedImageSrc} isLoading={true} error={null} />);
    expect(screen.getByText('Generating your try-on image with AI...')).toBeInTheDocument();
    expect(screen.queryByAltText('Generated Try-On')).not.toBeInTheDocument();
  });

  test('error state takes precedence over image src and loading state', () => {
    const errorMessage = 'Critical failure.';
    render(<TryOnDisplay generatedImageSrc={generatedImageSrc} isLoading={true} error={errorMessage} />);
    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    expect(screen.queryByText('Generating your try-on image with AI...')).not.toBeInTheDocument();
    expect(screen.queryByAltText('Generated Try-On')).not.toBeInTheDocument();
  });
});
