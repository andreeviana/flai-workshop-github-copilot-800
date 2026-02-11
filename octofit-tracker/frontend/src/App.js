import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Users from './components/Users';
import Teams from './components/Teams';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Workouts from './components/Workouts';


function Home() {
  return (
    <div className="container mt-4">
      <div className="jumbotron bg-light p-5 rounded">
        <h1 className="display-3 fw-bold">Welcome to OctoFit Tracker!</h1>
        <p className="lead fs-4">Your ultimate fitness tracking and team competition platform.</p>
        <hr className="my-4" />
        <p className="fs-5">Track your activities, compete with teams, and get personalized workout suggestions.</p>
        <div className="d-grid gap-3 d-sm-flex justify-content-sm-start mt-4">
          <Link to="/activities" className="btn btn-primary btn-lg px-4">
            🏃 Get Started
          </Link>
          <Link to="/leaderboard" className="btn btn-outline-primary btn-lg px-4">
            🏆 View Leaderboard
          </Link>
        </div>
      </div>

      <div className="row mt-5 g-4">
        <div className="col-md-4">
          <div className="card text-center h-100">
            <div className="card-body">
              <div className="fs-1 mb-3">📊</div>
              <h5 className="card-title">Track Activities</h5>
              <p className="card-text">Log your workouts and monitor your fitness progress over time.</p>
              <Link to="/activities" className="btn btn-sm btn-outline-primary">View Activities</Link>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-center h-100">
            <div className="card-body">
              <div className="fs-1 mb-3">👥</div>
              <h5 className="card-title">Join Teams</h5>
              <p className="card-text">Collaborate with others and compete in team challenges.</p>
              <Link to="/teams" className="btn btn-sm btn-outline-primary">Browse Teams</Link>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-center h-100">
            <div className="card-body">
              <div className="fs-1 mb-3">💪</div>
              <h5 className="card-title">Get Suggestions</h5>
              <p className="card-text">Receive personalized workout recommendations based on your goals.</p>
              <Link to="/workouts" className="btn btn-sm btn-outline-primary">View Workouts</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
          <div className="container-fluid">
            <Link className="navbar-brand fw-bold" to="/">
              <img src="/octofitapp-small.png" alt="OctoFit Logo" />
              <span className="fs-4">OctoFit Tracker</span>
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/">🏠 Home</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">👤 Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">👥 Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">📊 Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">🏆 Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">💪 Workouts</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/users" element={<Users />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
