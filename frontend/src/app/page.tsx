'use client';

import { useState } from "react";
import Image from "next/image";
import Tabs from "@/app/components/Tabs";
import TextGenerator from "@/app/components/TextGenerator";
import ImageGenerator from "@/app/components/ImageGenerator";
import AudioGenerator from "@/app/components/AudioGenerator";
import VideoGenerator from "@/app/components/VideoGenerator";

export default function Home() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [generatedText, setGeneratedText] = useState<string | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const handleTextGenerated = (text: string) => {
    setGeneratedText(text);
  };

  const handleImageGenerated = (url: string) => {
    setVideoUrl(null); // Clear video when a new image is generated
    setImageUrl(url);
  };

  const handleVideoGenerated = (url: string) => {
    setImageUrl(null); // Clear image when a new video is generated
    setVideoUrl(url);
  };

  const tabs = [
    { label: "Text", content: <TextGenerator onTextGenerated={handleTextGenerated} /> },
    { label: "Image", content: <ImageGenerator onImageGenerated={handleImageGenerated} /> },
    { label: "Audio", content: <AudioGenerator /> },
    { label: "Video", content: <VideoGenerator onVideoGenerated={handleVideoGenerated} /> },
  ];

  return (
    <main className="flex min-h-screen flex-col items-center p-4 bg-gray-900 text-white">
      <h1 className="text-5xl font-bold mb-8">OtakRot 🧠💥</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl">
        {/* Main Content */}
        <div className="md:col-span-2 bg-gray-800 p-4 rounded-lg flex items-center justify-center min-h-[400px]">
          {videoUrl ? (
            <video src={videoUrl} controls autoPlay className="max-w-full max-h-[400px] rounded-lg" />
          ) : imageUrl ? (
            <div className="relative">
              <img src={imageUrl} alt="Generated Meme" className="rounded-lg max-w-full h-auto" />
              {generatedText && (
                <div className="absolute bottom-4 left-4 right-4 bg-black bg-opacity-70 text-white text-center p-2 rounded">
                  <p className="text-xl font-bold">{generatedText}</p>
                </div>
              )}
            </div>
          ) : generatedText ? (
            <div className="text-white text-center p-4">
              <p className="text-2xl font-bold">{generatedText}</p>
            </div>
          ) : (
            <div className="text-gray-500">
              <p>Your generated meme will appear here.</p>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">Controls</h2>
          <Tabs tabs={tabs} />
        </div>
      </div>
    </main>
  );
}
