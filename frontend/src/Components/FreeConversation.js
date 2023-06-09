import AudioRecorder from "./AudioRecoder";
import ChatPrompt from "./ChatPrompt";
import { useState, useEffect, useRef } from "react";
import sound from "../assets/speech.mp3";

const FreeConversation = () => {
  const [gptmessage, setGpt] = useState("Bonjour clique sur start chat pour commencer un discussion avec moi");
  const [usermessage, setUser] = useState("");

  const play = () => {
    console.log("played");
    new Audio(sound).play();
  };

  return (
    <div className="h-screen w-full bg-gradient-to-b from-black to-gray-800 text-white">
      <div className="flex flex-col">
        <div className="flex mt-20 justify-center">
          <ChatPrompt name="AI" message={gptmessage} />
        </div>
        <div className="flex justify-center">
          <ChatPrompt name="User" message={usermessage} />
        </div>
      </div>
      <div className="mt-10">
        <AudioRecorder setGpt={setGpt} setUser={setUser} />
        <div className="flex justify-center">
          <button
            className="bg-cyan-950  text-white rounded p-2 m-3 hover:font-bold"
            onClick={play}
          >
            GPT answer
          </button>
        </div>
      </div>
    </div>
  );
};

export default FreeConversation;
