import AudioRecorder from "./AudioRecoder"
import ChatPrompt from "./ChatPrompt"
import { useState, useEffect, useRef } from 'react';
import sound from "../assets/speech.mp3"

const Home = (prop) => {
    const [gptmessage, setGpt] = useState("I am gpt");
    const [usermessage, setUser] = useState("I am User");

    const play = () => {
        console.log("played")
        new Audio(sound).play()
    }

    return (
        <div name='home' className="h-full w-full bg-gradient-to-b from-black to-gray-800 text-white">
            <div className='max-w-screen-lg mx-auto flex flex-col items-center justify-center h-full px-4'>
                <p>Welcome to the app to learn french with AI </p>
            </div>
        </div>
    )
}
export default Home