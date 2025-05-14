// src/App.jsx
import React, { useState,useRef, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [scale, setScale] = useState('');
  const [length, setLength] = useState('');
  const [fileUrl, setFileUrl] = useState('');
  const [error, setError] = useState('');
  const [chat, setChat] = useState([]);
  const [message, setMessage] = useState('');
  const chatEndRef = useRef(null);


  const scales = ['C Major','A Minor','G Major','E Minor','F Major','D Minor','D Major','B Minor','A Major','E Major','C Minor','G Minor','Bb Major','Eb Major','Ab Major','F# Minor','B Major','F# Major','Db Major','Ab Minor'];


  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const parsedLength = parseInt(length);
    if (!scale || isNaN(parsedLength) || parsedLength <= 0) {
      setError("Please select a scale and enter a valid numeric length.");
      return;
    }

    try {
      console.log(scale, parsedLength);
      const response = await axios.post('https://create-music-shapes-api.onrender.com/generate-music', {
        scale,
        length: parsedLength,
      }, { responseType: 'blob' });

      // Create a URL for the WAV file
      const file = new Blob([response.data], { type: 'audio/wav' });
      const fileUrl = URL.createObjectURL(file);
      setFileUrl(fileUrl);
    } catch (err) {
      setError('An error occurred, please try again.');
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    const newChat = [...chat, { sender: 'user', text: message }];
    setChat(newChat);
    setMessage('');

    try {
      const res = await axios.post('https://create-music-shapes-api.onrender.com/chat', {
        message: message,
      });

      const botReply = res.data.reply || "No response."; // Check for the actual response key
      setChat([...newChat, { sender: 'bot', text: botReply }]);
    } catch (err) {
      setChat([...newChat, { sender: 'bot', text: "Failed to get response." }]);
    }
  };
  useEffect(() => {
  chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
}, [chat]);

  return (
    <div className="min-h-screen bg-[url('/images/bg.jpg')] text-white font-sans bg-cover bg-no-repeat">
      {/* Navbar */}
      <nav className="bg-blue-800 h-20 shadow-lg flex items-center px-8">
        <div className="text-3xl font-semibold">MusicGen</div>
        <div className="ml-auto space-x-6 text-lg">
          <a href="#home" className="hover:text-indigo-300 transition">Home</a>
          <a href="#about" className="hover:text-indigo-300 transition">About</a>
          <a href="#contact" className="hover:text-indigo-300 transition">Contact</a>
        </div>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 px-20 justify-center py-20">
        {/* Music Generator Form */}
        <div className="bg-[#000000af] border border-[solid 2px white]  text-gray-800 p-8 rounded-xl shadow-2xl">
          <h1 className="text-4xl font-bold text-center text-white mb-6">Generate Music</h1>
          {error && <div className="text-red-500 text-center mb-4">{error}</div>}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="scale" className="block text-lg font-medium focus:outline-none focus:ring-0 text-gray-200">Select Scale</label>
              <select
                id="scale"
                name="scale"
                value={scale}
                onChange={(e) => setScale(e.target.value)}
                className="mt-2 p-3 bg-gray-900 text-white border border-gray-700 rounded-md w-full"
              >
                <option value="">Select a scale</option>
                {scales.map((s, i) => (
                  <option key={i} value={s.replace(" ", "_")}>{s}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="length" className="block text-lg font-medium text-gray-200">Note Length</label>
              <input
                type="number"
                id="length"
                name="length"
                value={length}
                onChange={(e) => setLength(e.target.value)}
                className="mt-2 p-3 bg-gray-900 text-white border border-gray-700 rounded-md w-full"
                placeholder="Enter number of notes"
                min="1"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition transform hover:scale-105"
            >
              Generate Music
            </button>
          </form>

          {fileUrl && (
            <div className="mt-6 text-center">
              <a
                href={fileUrl}
                download="generated-music.wav"
                className="bg-green-600 text-white py-3 px-6 rounded-md hover:bg-green-700 transition"
              >
                Download WAV File
              </a>
            </div>
          )}
        </div>

        {/* Chat Window */}
        <div className="bg-[#10182856] p-6 rounded-xl  flex flex-col h-[600px]" style={{
    boxShadow: "-2px 2px 5px rgba(255, 255, 255, 0.3)" // top-left shadow
  }}>     
          <div className=' flex justify-between px-5'>
          <h2 className="text-3xl font-semibold text-white mb-4">Talk to MusicBot</h2>
          <div className='flex gap-2'>
          <img src = "/images/notch.png" className='h-6 rounded-full'></img>
          <p>notch</p>
          </div>
          </div>
          <div className="flex-1 overflow-y-auto bg-[#e5e7eb46] rounded-md p-4 space-y-4">
            {chat.map((msg, idx) => (
              <div className={`w-full flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div key={idx} className={`p-3 rounded-md w-fit max-w-[75%] ${msg.sender === 'user' ? 'bg-blue-500' : 'bg-gray-700 self-start'}`}>
                <p className="text-md">{msg.text}</p>
              </div>
              <div ref={chatEndRef} />
              </div>
            ))}
          </div>
          <div className="flex mt-4 space-x-2">
            <form onSubmit={handleChatSubmit} className="flex mt-4 space-x-2  w-full">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="flex-1 p-3 bg-gray-700 text-white rounded-md "
              placeholder="Ask something..."
            />
            <button
              type='submit'
              className="px-5 py-3 bg-purple-600 rounded-md text-white hover:bg-purple-700 transition"
            >
              Send
            </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
