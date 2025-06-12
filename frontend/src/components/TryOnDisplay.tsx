// frontend/src/components/TryOnDisplay.tsx
interface TryOnDisplayProps {
  generatedImageSrc: string | null;
  isLoading: boolean;
  error: string | null;
}

export function TryOnDisplay({ generatedImageSrc, isLoading, error }: TryOnDisplayProps) {
  if (error) { // Error state checked first
    return (
      <div className="flex items-center justify-center w-full h-96 bg-red-50 rounded-lg shadow-inner p-4">
        <p className="text-red-600 text-center">Error: {error}</p>
      </div>
    );
  }

  if (isLoading) { // Loading state checked second
    return (
      <div className="flex flex-col items-center justify-center w-full h-96 bg-gray-100 rounded-lg shadow-inner">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mb-4"></div>
        <p className="text-gray-600">Generating your try-on image with AI...</p>
        <p className="text-sm text-gray-500">This may take a moment.</p>
      </div>
    );
  }

  if (!generatedImageSrc) {
    return (
      <div className="flex items-center justify-center w-full h-96 bg-gray-100 rounded-lg shadow-inner">
        <p className="text-gray-500">Select a model and a product, then click "Generate Try-On".</p>
      </div>
    );
  }

  return (
    <div className="relative w-full h-96 border rounded-lg overflow-hidden shadow-lg bg-gray-50">
      <img
        src={generatedImageSrc}
        alt="Generated Try-On"
        className="object-contain w-full h-full"
      />
    </div>
  );
}
