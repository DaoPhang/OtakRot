'use client';

import { useState } from 'react';

type ImageGeneratorProps = {
  onImageGenerated: (url: string) => void;
};

export default function ImageGenerator({ onImageGenerated }: ImageGeneratorProps) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      
      const data = await response.json();

      if (data && data.image_url) {
        onImageGenerated(data.image_url);
      } else if (data && data.error) {
        alert(`Backend Error: ${data.error}`);
      } else {
        alert("Received an unknown response format from the backend.");
      }

    } catch (error) {
      console.error('Error in handleGenerate (Image):', error);
      alert('Frontend failed to fetch the image from the backend. Check the browser console (F12) for detailed errors.');
    }
    setLoading(false);
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-2">Image Generation</h3>
      <textarea
        className="w-full p-2 rounded bg-gray-700 text-white"
        placeholder="Enter a prompt for the meme image..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="mt-2 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:bg-gray-500"
      >
        {loading ? 'Generating...' : 'Generate Image'}
      </button>
    </div>
  );
} 