import { useState, useEffect } from 'react'
import './styles/App.scss';
import axios from 'axios';

// Event handlers 
  const handleForwardClick = async() => {
    try {
          const response = await axios(
            { method: 'post',
            url: 'http://localhost:8080/forward'
            });
          console.log('Python response:', response.data);
        } catch (error) {
          console.error('Error calling Python backend:', error);
        }
  }; 

  const handleBackClick = async() => {
    try {
          const response = await axios(
            { method: 'post',
            url: 'http://localhost:8080/back'
            });
          console.log('Python response:', response.data);
        } catch (error) {
          console.error('Error calling Python backend:', error);
        }
  }; 

  const handleLeftClick = async() => {
    try {
          const response = await axios(
            { method: 'post',
            url: 'http://localhost:8080/turnleft'
            });
          console.log('Python response:', response.data);
        } catch (error) {
          console.error('Error calling Python backend:', error);
        }
  }; 

    const handleRightClick = async() => {
    try {
          const response = await axios(
            { method: 'post',
            url: 'http://localhost:8080/turnright'
            });
          console.log('Python response:', response.data);
        } catch (error) {
          console.error('Error calling Python backend:', error);
        }
  }; 


  const handleHeadRight = async() => {
    try {
          const response = await axios(
            { method: 'post',
            url: 'http://localhost:8080/turnheadright'
            });
          console.log('Python response:', response.data);
        } catch (error) {
          console.error('Error calling Python backend:', error);
        }
  }; 

  const handleHeadLeft = async() => {
    try {
          const response = await axios(
            { method: 'post',
            url: 'http://localhost:8080/turnheadleft'
            });
          console.log('Python response:', response.data);
        } catch (error) {
          console.error('Error calling Python backend:', error);
        }
  }; 
function ArrowButton({ direction, onClick }) {
  const arrowSymbol = {
    left: '&#8592;', // Left arrow
    right: '&#8594;', // Right arrow
    up: '&#8593;',   // Up arrow
    down: '&#8595;', // Down arrow
  };

  return (
    <button onClick={onClick} dangerouslySetInnerHTML={{ __html: arrowSymbol[''] }} />
  );
}

function ConnectButton() {
  const [isConnecting, setIsConnecting] = useState(false);
  const [connected, setConnected] = useState(false);
  const [dots, setDots] = useState("");

  useEffect(() => {
    if (!isConnecting) return;

    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
    }, 500);

    return () => clearInterval(interval);
  }, [isConnecting]);

  const handleConnectClick = async () => {
    setIsConnecting(true); // Start dots animation
    setConnected(false); // Reset "Connected!" if retrying

    try {
      const response = await axios.post("http://localhost:8080/connect");
      console.log("Python response:", response.data);
      setConnected(true);
    } catch (error) {
      console.error("Error calling Python backend:", error);
    } finally {
      setIsConnecting(false); // Stop dots animation
    }
  };

  const getButtonClass = () => {
    if (connected) return "connected";
    if (isConnecting) return "connecting";
    return "connect-btn";
  };

  return (
    <button className={getButtonClass()} 
            onClick={handleConnectClick} 
            disabled={isConnecting || connected}>
      {connected
        ? "Connected!"
        : isConnecting
        ? `Connecting${dots}`
        : "Connect"}
    </button>
  );
}

function App() {
  const [connection, setConnection] = useState(false); 
  const [prompt, setPrompt] = useState('');
  const handleInputChange = (event) => {
    setPrompt(event.target.value);
  };

  const handleEnterPress = async(event) => {
    if (event.key === 'Enter') {
      console.log('enter was pressed');
      console.log('prompt', prompt);
      try {
          const response = await axios.post('http://localhost:8080/chat', 
            prompt, {
            headers: {
              'Content-Type': 'application/json'
            }
          });
          // const data = await response.json();
          console.log('Chat sent to llama')
          setConnection(true)
          setPrompt('')
        } catch (error) {
          console.error('Error calling Python backend:', error);
        } 
    }};

  return (
    <>
      <div id="main">
      <h1>Droid Controller</h1>
        <div className='droid-image'>
        </div>
        <h2> DROID ARTURITO</h2>
           <ConnectButton />
          {/* <button className = "connect-btn" onClick={handleConnectClick}>Connect</button> */}
          <div className='controller'>
            <div className='arrows'>
              <div className='up'>
                <ArrowButton direction="up" onClick={handleForwardClick} />
              </div>
                <div className ="side-btns">
                  <div className='left'>
                    <ArrowButton direction="left" onClick={handleLeftClick} />
                  </div>
                  <div className ='arrow-placeholder'></div>
                  <div className='right'>
                    <ArrowButton direction="right" onClick={handleRightClick} />
                  </div>
                </div>
                <div className='down'>
                  <ArrowButton direction="down" onClick={handleBackClick} />
                </div>
            </div>
            <div className ='head-arrows'>
              <div className = 'left'>
                <ArrowButton direction="left" onClick={handleHeadLeft} />
              </div>
                  <div className ='arrow-placeholder'></div>
              <div className = 'right'>
                <ArrowButton direction="right" onClick={handleHeadRight} />
              </div>
            </div>
        </div>

          <div className = 'chat'>
            <label for="name">Chat:</label>
            <input
                type="text"
                id="prompt"
                value = {prompt}
                onChange = {handleInputChange}
                onKeyDown={handleEnterPress}
                name="prompt"
                minlength="2"
                maxlength="100"
                size="10" />
          </div>
      </div>

    </>
  )
}

export default App
