import { Link, useMatch, useResolvedPath } from "react-router-dom";
import { FaBars } from "react-icons/fa";

import React from "react";

export default function Navbar() {
  const links = [
    {
      id: 1,
      name: "Free Conversation",
      link: "free",
    },
    {
      id: 2,
      name: "Guided Conversation",
      link: "guided",
    },
    {
      id: 3,
      name: "Login",
      link: "login",
    },
    {
      id: 4,
      name: "Register",
      link: "register",
    },
  ];
  return (
    <div className=" text-white bg-black w-full ">
      <nav>
        <Link to="/" className=" flex justifiy-start text-5xl ml-2">
          SpeakIt
        </Link>
        <ul className="flex justify-end ">
          {links.map(({ id, link, name }) => (
            <Link
              to={link}
              key={id}
              className="mr-4  cursor-pointer capitalize font-medium hover:font-bold"
            >
              {name}{" "}
            </Link>
          ))}
        </ul>
      </nav>
    </div>
  );
}

function CustomLink({ to, children, ...props }) {
  const resolvedPath = useResolvedPath(to);
  const isActive = useMatch({ path: resolvedPath.pathname, end: true });

  return (
    <li className={isActive ? "active" : ""}>
      <Link to={to} {...props}>
        {children}
      </Link>
    </li>
  );
}
