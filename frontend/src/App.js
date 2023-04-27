import "./App.css";
import Navbar from "./Components/NavBar";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Components/Home";
import GuidedConversation from "./Components/GuidedConversation";
import FreeConversation from "./Components/FreeConversation";
import Login from "./Components/Login";
import Register from "./Components/Register";

const App = () => {
  var ws = null;

  // TODO:
  // Use webSocket connection and rerender at any change of the connection --> should be
  // implemented very soon

  // useEffect(() => {
  //   ws = new WebSocket("ws://localhost:8000/ws")
  //   ws.onopen = () => ws.send("Hello from client")
  //   ws.onmessage = (e) => { console.log(e) }
  // }, [ws])

  return (
    <>
      <div className="text-black h-screen text-sm flex flex-col items-start">
        <BrowserRouter>
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/guided" element={<GuidedConversation />} />
            <Route path="/free" element={<FreeConversation />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </BrowserRouter>
      </div>
    </>
  );
};

export default App;
