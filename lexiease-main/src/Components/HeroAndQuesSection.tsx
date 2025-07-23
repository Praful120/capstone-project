
// import image1 from '../assets/image1.svg';
// export default function HeroAndQuesSection() {
//   return (
//     <div className="flex flex-col items-center justify-center  bg-white mt-10 p-6">
//       <h1 className="text-3xl font-extrabold text-center mb-4">
//         Ready to simplify your text?
//       </h1>
      
//         <div className="flex justify-center">
//         <button className="bg-[#ef8354] contecnt-center text-white font-bold px-8 py-2 rounded-md cursor-pointer shadow-md hover:bg-orange-600 transition">Summarize</button>
//         </div>

//         <div className="flex justify-center mt-15">
//       <img
//         src= {image1} 
//         alt="Confused brain mascot"
//         className="w-full h-full object-contain"
//       />
//     </div>
//       </div>
      
      
//   )
// }

import { useState, useRef } from "react";
import image1 from '../assets/image1.svg';

export default function HeroAndQuesSection() {
  // State for the input text, summary, file, and loading status
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // State to hold the audio data URL
  const [audioSrc, setAudioSrc] = useState("");
  // Ref to control the audio element
  const audioRef = useRef<HTMLAudioElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  // Function to handle the summarization request
  const handleSubmit = async () => {
    if (!text.trim() && !file) {
      alert("Please enter text or upload a file.");
      return;
    }

    setIsLoading(true);
    setSummary("");
    setAudioSrc(""); 

    const formData = new FormData();
    if (file) {
      formData.append("file", file);
    }

    try {
      let response;
      // Use the endpoint that provides audio when summarizing text
      if (text.trim()) {
        response = await fetch("http://127.0.0.1:8000/summarize-and-speak", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        });
      } else {
        // File upload uses its own endpoint (modify if you want TTS for files too)
        response = await fetch("http://127.0.0.1:8000/upload-and-summarize", {
          method: "POST",
          body: formData,
        });
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSummary(data.summary);

      // Check for audio data and create a playable URL
      if (data.audio_base64) {
        const audioDataUrl = `data:audio/mp3;base64,${data.audio_base64}`;
        setAudioSrc(audioDataUrl);
      }

    } catch (error) {
      console.error("Error summarizing:", error);
      alert("Failed to get summary. Please check the console for details.");
    } finally {
      setIsLoading(false);
    }
  };

  // Function to play the generated audio
  const playAudio = () => {
    if (audioRef.current) {
      audioRef.current.play();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center bg-white mt-10 p-6 w-full">
      <div className="w-full max-w-4xl">
        {/* Input Section */}
        <div className="bg-gray-100 p-6 rounded-lg shadow-lg">
          <h1 className="text-3xl font-extrabold text-center mb-4 text-black">
            Ready to simplify your text?
          </h1>
          <textarea
            className="w-full p-3 border rounded-md text-black"
            rows={8}
            placeholder="Enter your text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          ></textarea>
          <div className="flex flex-col sm:flex-row justify-between items-center mt-4 gap-4">
            <input type="file" onChange={handleFileChange} className="text-black" />
            <button
              onClick={handleSubmit}
              className="bg-[#ef8354] hover:bg-orange-600 text-white font-bold py-2 px-8 rounded-md cursor-pointer shadow-md transition w-full sm:w-auto disabled:bg-gray-400"
              disabled={isLoading}
            >
              {isLoading ? "Summarizing..." : "Summarize"}
            </button>
          </div>
        </div>
        
        {/* Output Section */}
        {summary && (
          <div className="bg-gray-100 p-6 rounded-lg shadow-lg mt-6 text-black">
            <h2 className="text-2xl font-bold mb-2">Summary</h2>
            <p>{summary}</p>
            
            {/* Audio player section */}
            {audioSrc && (
              <div className="mt-4">
                <button 
                  onClick={playAudio}
                  className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                  ▶️ Play Audio
                </button>
                <audio ref={audioRef} src={audioSrc} className="hidden" />
              </div>
            )}
          </div>
        )}
      </div>

      {/* Image Section */}
      <div className="flex justify-center mt-10">
        <img
          src={image1} 
          alt="Confused brain mascot"
          className="w-full max-w-lg h-auto object-contain"
        />
      </div>
    </div>
  );
}
