import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [feedTimes, setFeedTimes] = useState(0);
  const [feedTime, setFeedTime] = useState(0);
  const [isReadyToPlay, setIsReadyToPlay] = useState(false);

  // Check if the conditions are met to enable the Play button
  useEffect(() => {
    setIsReadyToPlay(feedTimes > 0 && feedTime > 0);
  }, [feedTimes, feedTime]);

  const handleFeedTimes = () => {
    const times = prompt("How many feed rounds do you want to set?");
    if (!isNaN(times) && times) {
      const newTimes = parseInt(times, 10);
      setFeedTimes(newTimes);
      sendFeedData(newTimes, feedTime);
    }
  };

  const increaseFeedTimes = () => {
    const newFeedTimes = feedTimes + 1;
    setFeedTimes(newFeedTimes);
    sendFeedData(newFeedTimes, feedTime);
  };

  const decreaseFeedTimes = () => {
    const newFeedTimes = Math.max(0, feedTimes - 1);
    setFeedTimes(newFeedTimes);
    sendFeedData(newFeedTimes, feedTime);
  };

  const handleFeedTimeChange = (event) => {
    const newFeedTime = parseInt(event.target.value, 10);
    setFeedTime(newFeedTime);
    sendFeedData(feedTimes, newFeedTime);
  };

  const sendFeedData = (times, time) => {
    axios.post('http://172.20.10.11:5000/start', { 
      rounds:times, 
      time:time 
      })
      .then(response => {
        console.log('Settings updated successfully!');
        console.log(response.data);
      })
      .catch(error => console.error('Failed to update settings:', error));
  };

  const handlePlay = () => {
    console.log("Play: Feeding starts with", { feedTimes, feedTime });
    // Implement the function to start feeding mechanism
  };

  return (
    <div className={`App ${feedTimes === 7 ? 'special-background' : ''}`}>
      <img src="/Nemo.png" alt="Fish Feeder Title" style={{ maxWidth: '1000px' }} />
      <button onClick={handleFeedTimes}>Feed Rounds</button>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '10px' }}>
        <button onClick={increaseFeedTimes}>UpUp!!</button>
        <button onClick={decreaseFeedTimes}>Nahh</button>
      </div>
      <p>Feed rounds per day: {feedTimes}</p>
      <p>Feeding time: {feedTime} hour{feedTime !== 1 ? 's' : ''}</p>
      <label>
        Set feeding time (0-24 hours):
        <input
          type="range"
          min="0"
          max="24"
          value={feedTime}
          onChange={handleFeedTimeChange}
        />
      </label>
      <button onClick={handlePlay} disabled={!isReadyToPlay}>Play</button>
    </div>
  );
}

export default App;
