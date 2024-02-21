// eslint-disable-next-line no-unused-vars
import React from 'react'
import './App.css'
import HeaderContent from './components/HeaderContent/HeaderContent'
import SidebarContent from './components/SidebarContent/SidebarContent'
import BodyContent from './components/BodyContent/BodyContent'

export default function App() {
  return (
    <div className="grid-container">
      <HeaderContent/>
      <SidebarContent/>
      <BodyContent/>
    </div>
  )
}
