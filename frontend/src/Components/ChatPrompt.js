import { useEffect } from "react";


const ChatPrompt = (props) => {

    return (
        <div className="w-1/2">
            <p className="font-bold my-3">{props.name} Prompt</p>
            <div className="border-2 rounded  py-10 px-4 bottom-5 w-100  bg-cyan-950  hover:italic">
                {props.message}
            </div>
        </div>
    )
}
export default ChatPrompt;