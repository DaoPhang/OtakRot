'use client';

import { useState } from 'react';

type TextGeneratorProps = {
  onTextGenerated: (text: string) => void;
};

export default function TextGenerator({ onTextGenerated }: TextGeneratorProps) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/generate-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      onTextGenerated(data.text || data.error || 'An unknown error occurred.');
    } catch (error) {
      console.error('Error generating text:', error);
      onTextGenerated('Failed to connect to the server.');
    }
    setLoading(false);
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-2">Text Generation</h3>
      <textarea
        className="w-full p-2 rounded bg-gray-700 text-white"
        placeholder="Enter a prompt for the meme text..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="mt-2 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:bg-gray-500"
      >
        {loading ? 'Generating...' : 'Generate Text'}
      </button>
    </div>
  );
} 