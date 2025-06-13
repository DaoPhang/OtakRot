'use client';

import { useState } from 'react';

export default function TextGenerator() {
  const [prompt, setPrompt] = useState('');
  const [generatedText, setGeneratedText] = useState('');

  const handleGenerate = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/generate-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      setGeneratedText(data.text);
    } catch (error) {
      console.error('Error generating text:', error);
    }
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
        className="mt-2 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Generate Text
      </button>
      {generatedText && (
        <div className="mt-4 p-2 bg-gray-700 rounded">
          <p className="text-white">{generatedText}</p>
        </div>
      )}
    </div>
  );
} 