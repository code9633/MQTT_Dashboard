// eslint-disable-next-line no-unused-vars
import React from "react";
import "./HeaderContent.css";
import { BsFillEnvelopeFill } from "react-icons/bs";


export default function HeaderContent() {
  return (
    <header className="header">
      <h1>MQTT Dashboard</h1>
      <BsFillEnvelopeFill className="notification" />
    </header>
  );
}
