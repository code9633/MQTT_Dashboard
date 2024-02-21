// eslint-disable-next-line no-unused-vars
import React from 'react'
import "./SidebarContent.css"
import {BsGrid1X2Fill}  from "react-icons/bs"


export default function SidebarContent() {
  return (
    <div className='sidebar'>
      <div className='brandName'>
        <h3>Solar Cast</h3>
      </div>
      <div className="sidebarList">
        <li className='sidebar-list-item'>
          <a href="">
            <BsGrid1X2Fill className='icon'/> Dashboard
          </a>
        </li>
      </div>
    </div>
  )
}
