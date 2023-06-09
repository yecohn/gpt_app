import AudioRecorder from "./AudioRecoder";
import ChatPrompt from "./ChatPrompt";
import { useState, useEffect, useRef } from "react";
import sound from "../assets/speech.mp3";
import YoutubeEmbed from "./YoutubeEmbed";
import {
  Chat,
  Channel,
  ChannelHeader,
  MessageInput,
  MessageList,
  Thread,
  Window,
} from "stream-chat-react";

const GuidedConversation = (prop) => {
  const [gptmessage, setGpt] = useState("I am gpt");
  const [usermessage, setUser] = useState("I am User");

  const play = () => {
    console.log("played");
    new Audio(sound).play();
  };

  const sendPrompt = () => {
    setGpt("Que ce passe t'il  dans la video ?");
  };

return (
  <>
    <div className="bg-gradient-to-b from-black to-gray-800 text-white">
      <div className="mt-20">
        Welcome to the guided conversation page. This is page is made to help
        you learn french with AI around specific topics. here the list of
        topic to get started with. We propose you to get started by watching
        the video and the click the button start to start talking about the
        video.
      </div>
      <div className="w-full">
        <div className="h-20 w-full flex justify-center mt-20 hover:font-bold ">
          Le petit Prince Topic
        </div>
        <div className=" h-full w-full flex justify-center mb-20">
          <YoutubeEmbed embedId="cjr2aaZpABo" />
        </div>
      </div>
      <div className="">
        <AudioRecorder setGpt={setGpt} setUser={setUser} />
        <div className="flex justify-center">
          <button
            className="bg-cyan-950 text-white rounded p-2 m-3 hover:font-bold"
            onClick={play}
          >
            Voice answer
          </button>
        </div>
      </div>
      <div className="flex justify-center">
        <ChatPrompt name="AI" message={gptmessage} />
      </div>
      <div className="flex justify-center">
        <ChatPrompt name="User" message={usermessage} />
      </div>
    </div>
  </>
);
  return (
    <Chat client={prop.client}>
      <Channel>
        <Window>
          <ChannelHeader />
          <MessageList />
          <MessageInput />
        </Window>
        <Thread />
      </Channel>
    </Chat>
  );
};

export default GuidedConversation;


