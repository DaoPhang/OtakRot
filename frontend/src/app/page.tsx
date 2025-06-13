import Image from "next/image";
import Tabs from "@/app/components/Tabs";
import TextGenerator from "@/app/components/TextGenerator";
import ImageGenerator from "@/app/components/ImageGenerator";
import AudioGenerator from "@/app/components/AudioGenerator";
import VideoGenerator from "@/app/components/VideoGenerator";

export default function Home() {
  const tabs = [
    { label: "Text", content: <TextGenerator /> },
    { label: "Image", content: <ImageGenerator /> },
    { label: "Audio", content: <AudioGenerator /> },
    { label: "Video", content: <VideoGenerator /> },
  ];

  return (
    <main className="flex min-h-screen flex-col items-center p-4 bg-gray-900 text-white">
      <h1 className="text-5xl font-bold mb-8">OtakRot 🧠💥</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl">
        {/* Main Content */}
        <div className="md:col-span-2 bg-gray-800 p-4 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">Generated Meme</h2>
          {/* Meme display will go here */}
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
