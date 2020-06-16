import React, { useEffect, useState, useRef } from 'react'
import './Modal.css'

export default function Modal({ show, connEstablished, callback }) {
  const uriRef = useRef(null)
  const portRef = useRef(null)
  const [display, setDisplay] = useState(show ? 'block' : 'none')

  useEffect(() => {
    setDisplay(show ? 'block' : 'none')
  }, [show])

  return (
    <div className='modal' style={{ display: display }}>
      <div className='modal-content'>
        <div>
          <b>Server information</b>
        </div>
        <div>
          <div>
            <hr />
            <p>Enter the remote ip and port</p>
            <span>
              <input
                placeholder='URI'
                ref={uriRef} type="text"
                style={{ 'marginRight': '20px' }} />
              <input placeholder='Port' ref={portRef} type="text" />
            </span>
          </div>
          <div className='footer'>
            <hr />
            {
              connEstablished ? <></> : <b>Could not connect !</b>
            }
            <button
              onClick={() => {
                callback(uriRef.current.value, portRef.current.value)
              }}>Save</button>
          </div>
        </div>
      </div>
    </div>
  )
}