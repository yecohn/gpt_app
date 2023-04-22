import { useEffect } from "react";


const ChatPrompt = (props) => {

    return (
        <div>
            <p className="font-bold">{props.name} Prompt</p>
            <div className="border-2 rounded  py-8 px-4 bottom-5 w-100 border-rose-500  hover:italic">
                {props.message}
            </div>
        </div>
    )
}
export default ChatPrompt;