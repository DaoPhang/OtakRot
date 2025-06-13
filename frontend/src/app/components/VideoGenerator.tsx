'use client';

import { useState } from 'react';

type VideoGeneratorProps = {
  onVideoGenerated: (url: string) => void;
};

export default function VideoGenerator({ onVideoGenerated }: VideoGeneratorProps) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/generate-video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      if (data.video_url) {
        onVideoGenerated(data.video_url);
      } else if (data.error) {
        alert(`Error: ${data.error}`);
      }
    } catch (error) {
      console.error('Error generating video:', error);
      alert('Failed to connect to the server for video generation.');
    }
    setLoading(false);
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-2">Video Generation</h3>
      <textarea
        className="w-full p-2 rounded bg-gray-700 text-white"
        placeholder="Enter a prompt for the video..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="mt-2 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:bg-gray-500"
      >
        {loading ? 'Generating...' : 'Generate Video'}
      </button>
    </div>
  );
} 