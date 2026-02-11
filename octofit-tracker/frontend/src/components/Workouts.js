import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const codespace = process.env.REACT_APP_CODESPACE_NAME;
        const apiUrl = codespace 
          ? `https://${codespace}-8000.app.github.dev/api/workouts/`
          : 'http://localhost:8000/api/workouts/';
        
        console.log('Fetching workouts from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Workouts API response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Processed workouts data:', workoutsData);
        
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="text-center">
          <div className="spinner-border text-light" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="text-light mt-3">Loading workouts...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h1 className="display-4">💪 Workout Suggestions</h1>
        <p className="lead">Personalized workout plans and exercises</p>
      </div>
      
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <h3 className="mb-0">Available Workouts</h3>
          <button className="btn btn-light btn-sm">🔄 Refresh</button>
        </div>
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-striped table-hover mb-0">
              <thead className="table-dark">
                <tr>
                  <th>Workout Name</th>
                  <th>Description</th>
                  <th>Duration (min)</th>
                  <th>Difficulty</th>
                </tr>
              </thead>
              <tbody>
                {workouts.length > 0 ? (
                  workouts.map((workout) => (
                    <tr key={workout.id || workout._id}>
                      <td><strong>{workout.name}</strong></td>
                      <td>{workout.description || 'No description available'}</td>
                      <td><span className="badge bg-info">{workout.duration || 'N/A'} min</span></td>
                      <td>
                        <span className={`badge ${
                          workout.difficulty === 'Hard' ? 'bg-danger' : 
                          workout.difficulty === 'Medium' ? 'bg-warning text-dark' : 
                          'bg-success'
                        }`}>
                          {workout.difficulty || 'N/A'}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4">
                      <div className="empty-state">
                        <div className="empty-state-icon">💪</div>
                        <p>No workout suggestions available. Check back soon!</p>
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Workouts;
