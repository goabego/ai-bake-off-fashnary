'use client';

import { useEffect, useState } from 'react';
import { ProductCard } from '@/components/ProductCard';
import { ProductDisplay } from '@/types/product';
import { motion } from 'framer-motion';
import { TryOnDisplay } from '@/components/TryOnDisplay'; // Added
import { User, UserDisplay } from '@/types/user'; // Added

// Define the backend URL
const API_BASE_URL = 'https://backend-879168005744.us-west1.run.app'; // Added

export default function Home() {
  const [products, setProducts] = useState<ProductDisplay[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  // New state variables for user selection and try-on
  const [users, setUsers] = useState<User[]>([]); // Added
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null); // Added
  const [selectedUserDisplay, setSelectedUserDisplay] = useState<UserDisplay | null>(null); // Added
  const [selectedProduct, setSelectedProduct] = useState<ProductDisplay | null>(null); // Added
  const [loadingUsers, setLoadingUsers] = useState(true); // Added
  const [userError, setUserError] = useState<string | null>(null); // Added

  // New state variables for AI image generation
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [generationError, setGenerationError] = useState<string | null>(null);
  const [generatedTryOnImage, setGeneratedTryOnImage] = useState<string | null>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;

    const fetchProducts = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/products`); // Updated API URL
        const data = await response.json();
        
        const displayData = await Promise.all(
          data.map(async (product: any) => {
            const displayResponse = await fetch(
              `${API_BASE_URL}/products/${product.id}/display` // Updated API URL
            );
            return displayResponse.json();
          })
        );
        
        setProducts(displayData);
      } catch (err) {
        setError('Failed to fetch products');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [mounted]);

  // Fetch users
  useEffect(() => {
    if (!mounted) return;
    const fetchUsers = async () => {
      try {
        setLoadingUsers(true);
        const response = await fetch(`${API_BASE_URL}/users`); // Added
        const data = await response.json();
        setUsers(data);
        setUserError(null); // Clear previous errors
      } catch (err) {
        setUserError('Failed to fetch users');
        console.error(err);
      } finally {
        setLoadingUsers(false);
      }
    };
    fetchUsers();
  }, [mounted]);

  // Fetch selected user display data
  useEffect(() => {
    if (!mounted || !selectedUserId) {
      setSelectedUserDisplay(null); // Clear previous user display
      return;
    }
    const fetchUserDisplay = async () => {
      try {
        // setLoadingUsers(true); // Reuse loading state or create a new one for selected user
        // Let's use a specific loading state for the display if it becomes slow
        const response = await fetch(`${API_BASE_URL}/users/${selectedUserId}/display`); // Added
        const data = await response.json();
        setSelectedUserDisplay(data);
        setUserError(null); // Clear previous errors
      } catch (err) {
        setUserError(`Failed to fetch display data for user ${selectedUserId}`);
        console.error(err);
        setSelectedUserDisplay(null); // Clear on error
      } finally {
        // setLoadingUsers(false);
      }
    };
    fetchUserDisplay();
  }, [mounted, selectedUserId]);

  if (!mounted) {
    return null;
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-white to-gray-50">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary border-t-transparent"></div>
          <p className="text-lg text-gray-600">Loading our collection...</p>
        </div>
      </div>
    );
  }

  // Combined error display for products and users, or handle separately if preferred
  if (error || userError) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-white to-gray-50">
        <div className="text-destructive text-xl bg-white p-8 rounded-lg shadow-lg">
          {error && <p>{error}</p>}
          {userError && <p>{userError}</p>}
        </div>
      </div>
    );
  }

  const categories = ['all', ...new Set(products.map(p => p.type.toLowerCase()))];
  const filteredProducts = selectedCategory === 'all' 
    ? products 
    : products.filter(p => p.type.toLowerCase() === selectedCategory);

  const parseDataUrl = (dataUrl: string): { base64Data: string; mimeType: string } | null => {
    const match = dataUrl.match(/^data:(image\/\w+);base64,(.*)$/);
    if (!match) return null;
    return { mimeType: match[1], base64Data: match[2] };
  };

  const handleTryOn = async () => {
    if (!selectedUserDisplay || !selectedProduct) {
      alert("Please select both a user model and a product.");
      return;
    }

    setIsGeneratingImage(true);
    setGenerationError(null);
    setGeneratedTryOnImage(null); // Clear previous image

    const userImgData = parseDataUrl(selectedUserDisplay.image);
    const productImgData = parseDataUrl(selectedProduct.image);

    if (!userImgData || !productImgData) {
      setGenerationError("Could not parse image data. Ensure images are loaded correctly.");
      setIsGeneratingImage(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/tryon/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_image_base64: userImgData.base64Data,
          user_image_mimetype: userImgData.mimeType,
          product_image_base64: productImgData.base64Data,
          product_image_mimetype: productImgData.mimeType,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred during generation.' }));
        throw new Error(errorData.detail || `API request failed with status ${response.status}`);
      }

      const result = await response.json();
      setGeneratedTryOnImage(result.generated_image_base64);

    } catch (err) {
      if (err instanceof Error) {
        setGenerationError(err.message);
      } else {
        setGenerationError('An unknown error occurred.');
      }
      console.error("Try-on generation error:", err);
    } finally {
      setIsGeneratingImage(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold text-center bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
            Fashnary Staging Environment
          </h1>
          <p className="text-center text-gray-600 mt-2">
            Discover our curated collection of fashion essentials
          </p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="flex flex-wrap justify-center gap-2 mb-8">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all
                ${selectedCategory === category
                  ? 'bg-primary text-white shadow-md'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
                }`}
            >
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>

        {/* New Try-On Section */}
        <section className="container mx-auto px-4 py-8 grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
          <div>
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">Select Model</h2>
            {loadingUsers && <p>Loading users...</p>}
            {/* userError is handled globally now, but can be specific here if needed */}
            {!loadingUsers && users.length > 0 && (
              <select
                value={selectedUserId || ''}
                onChange={(e) => setSelectedUserId(e.target.value)}
                className="w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="" disabled>Select a user</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.name}
                  </option>
                ))}
              </select>
            )}
            {!loadingUsers && users.length === 0 && !userError && (
              <p className="text-gray-500">No users available.</p>
            )}

            {selectedUserDisplay && !loadingUsers && ( // Show only if not loading users (initial load)
               <div className="mt-4 p-4 border rounded-lg bg-gray-50 shadow">
                 <h3 className="text-lg font-medium text-gray-700">{selectedUserDisplay.name}</h3>
                 {/* Optional: Display user description or other details */}
                 {selectedUserDisplay.description && <p className="text-sm text-gray-600">{selectedUserDisplay.description}</p>}
               </div>
             )}
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">Virtual Try-On</h2>
            <TryOnDisplay
              generatedImageSrc={generatedTryOnImage}
              isLoading={isGeneratingImage}
              error={generationError}
            />
            <div className="mt-6 text-center">
              <button
                onClick={handleTryOn}
                disabled={isGeneratingImage || !selectedUserDisplay || !selectedProduct}
                className="px-8 py-3 bg-gradient-to-r from-primary to-purple-600 text-white font-semibold rounded-lg shadow-md hover:from-primary-dark hover:to-purple-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGeneratingImage ? 'Generating...' : 'Generate AI Try-On'}
              </button>
            </div>
            {selectedProduct && !generatedTryOnImage && !isGeneratingImage && !generationError && ( // Show selected product only if no AI image/loading/error
               <div className="mt-4 p-4 border rounded-lg bg-gray-50 shadow">
                 <h3 className="text-lg font-medium text-gray-700">Selected Product (for AI generation):</h3>
                 <p className="text-sm text-gray-600">{selectedProduct.name} - {selectedProduct.description}</p>
                 <p className="font-semibold text-primary">{selectedProduct.price}</p>
               </div>
            )}
          </div>
        </section>

        {/* Existing Product Listing */}
        <h2 className="text-3xl font-semibold text-center text-gray-800 my-8 pt-8 border-t">
          Our Products
        </h2>
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {filteredProducts.map((product, index) => (
            <motion.div
              key={product.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              onClick={() => setSelectedProduct(product)} // Select product on click
              className="cursor-pointer" // Add cursor pointer for better UX
            >
              <ProductCard product={product} />
            </motion.div>
          ))}
        </motion.div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">
              No products found in this category
            </p>
          </div>
        )}
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-gray-600">
            © 2024 Fashnary. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
} 