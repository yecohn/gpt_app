import './App.css';
import AudioRecorder from './Components/AudioRecoder';
import ChatPrompt from './Components/ChatPrompt';
import sound from "./assets/speech.mp3"
import { useState, useEffect, useRef } from 'react';
import image from "./assets/background.jpg"

function App() {
  const [gptmessage, setGpt] = useState("I am gpt");
  const [usermessage, setUser] = useState("I am User");
  var ws = null

  // TODO:
  // Use webSocket connection and rerender at any change of the connection --> should be
  // implemented very soon 

  // useEffect(() => {
  //   ws = new WebSocket("ws://localhost:8000/ws")
  //   ws.onopen = () => ws.send("Hello from client")
  //   ws.onmessage = (e) => { console.log(e) }
  // }, [ws])

  const styles = {
    backgroundImage: `url(${image})`,
    // backgroundPosition: 'center',
    // backgroundSize: 'cover',
    // backgroundRepeat: 'no-repeat',
    // width: '100vw',
    // height: '100vh'
  };

  const play = () => {
    console.log("played")
    new Audio(sound).play()
  }



  return (
    <div style={{ backgroundImage: `url(${image})`, backgroundSize: `cover` }} className='text-black text-sm grid grid-rows-4 grid-cols-3 h-full w-full' >
      <div className='row-start-1 row-end-2 col-start-1 col-span-3 text-xl flex justify-center'> Learn French with AI
      </div>
      <div className='row-start-2 row-span-1 col-start-1 col-span-3'>
        <AudioRecorder setGpt={setGpt} setUser={setUser} />
        <div className='flex justify-center'>
          <button className='bg-sky-500 text-white rounded p-2 m-3 hover:font-bold' onClick={play}>GPT answer</button>
        </div>
      </div>
      <div className='row-start-3 row-span-1 col-start-2 col-span-1'>
        <ChatPrompt name="GPT" message={gptmessage} />
      </div>
      <div className='row-start-4 row-span-1 col-start-2 col-span-1'>
        <ChatPrompt name="User" message={usermessage} />
      </div>
    </div>
  );


}

export default App;
