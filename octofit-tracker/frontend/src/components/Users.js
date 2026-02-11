import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    role: '',
    team_id: ''
  });
  const [saveError, setSaveError] = useState(null);
  const [saving, setSaving] = useState(false);

  const getApiUrl = (endpoint) => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    return codespace 
      ? `https://${codespace}-8000.app.github.dev/api/${endpoint}/`
      : `http://localhost:8000/api/${endpoint}/`;
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch users
        const usersResponse = await fetch(getApiUrl('users'));
        if (!usersResponse.ok) {
          throw new Error(`HTTP error! status: ${usersResponse.status}`);
        }
        const usersData = await usersResponse.json();
        const processedUsers = usersData.results || usersData;
        setUsers(Array.isArray(processedUsers) ? processedUsers : []);

        // Fetch teams
        const teamsResponse = await fetch(getApiUrl('teams'));
        if (teamsResponse.ok) {
          const teamsData = await teamsResponse.json();
          const processedTeams = teamsData.results || teamsData;
          setTeams(Array.isArray(processedTeams) ? processedTeams : []);
        }

        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleEditClick = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name || '',
      email: user.email || '',
      role: user.role || 'member',
      team_id: user.team_id || ''
    });
    setSaveError(null);
    setShowEditModal(true);
  };

  const handleCloseModal = () => {
    setShowEditModal(false);
    setEditingUser(null);
    setFormData({ name: '', email: '', role: '', team_id: '' });
    setSaveError(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    if (!editingUser) return;

    setSaving(true);
    setSaveError(null);

    try {
      const updateData = {
        name: formData.name,
        email: formData.email,
        role: formData.role,
        team_id: formData.team_id === '' ? null : parseInt(formData.team_id)
      };

      const response = await fetch(getApiUrl(`users/${editingUser.id}`), {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update user');
      }

      const updatedUser = await response.json();
      
      // Update the users list with the updated user
      setUsers(users.map(u => u.id === updatedUser.id ? updatedUser : u));
      
      handleCloseModal();
    } catch (error) {
      console.error('Error saving user:', error);
      setSaveError(error.message);
    } finally {
      setSaving(false);
    }
  };

  const getTeamName = (teamId) => {
    const team = teams.find(t => t.id === teamId);
    return team ? team.name : `Team ${teamId}`;
  };

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="text-center">
          <div className="spinner-border text-light" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="text-light mt-3">Loading users...</p>
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
        <h1 className="display-4">👤 Users</h1>
        <p className="lead">Manage and view user profiles</p>
      </div>
      
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <h3 className="mb-0">All Users</h3>
          <button className="btn btn-light btn-sm">+ Add User</button>
        </div>
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-striped table-hover mb-0">
              <thead className="table-dark">
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Team</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.length > 0 ? (
                  users.map((user) => (
                    <tr key={user.id || user._id}>
                      <td><strong>{user.name}</strong></td>
                      <td>{user.email}</td>
                      <td>
                        <span className="badge bg-secondary">{user.role || 'member'}</span>
                      </td>
                      <td>
                        {user.team_id ? (
                          <span className="badge bg-primary">{getTeamName(user.team_id)}</span>
                        ) : (
                          <span className="text-muted">No team</span>
                        )}
                      </td>
                      <td>
                        <button 
                          className="btn btn-sm btn-outline-primary"
                          onClick={() => handleEditClick(user)}
                        >
                          ✏️ Edit
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5">
                      <div className="empty-state">
                        <div className="empty-state-icon">👤</div>
                        <p>No users found</p>
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Edit User Modal */}
      {showEditModal && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit User</h5>
                <button 
                  type="button" 
                  className="btn-close" 
                  onClick={handleCloseModal}
                  disabled={saving}
                ></button>
              </div>
              <div className="modal-body">
                {saveError && (
                  <div className="alert alert-danger" role="alert">
                    {saveError}
                  </div>
                )}
                <form>
                  <div className="mb-3">
                    <label htmlFor="name" className="form-label">Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="role" className="form-label">Role</label>
                    <select
                      className="form-select"
                      id="role"
                      name="role"
                      value={formData.role}
                      onChange={handleInputChange}
                    >
                      <option value="member">Member</option>
                      <option value="admin">Admin</option>
                      <option value="coach">Coach</option>
                    </select>
                  </div>
                  <div className="mb-3">
                    <label htmlFor="team_id" className="form-label">Team</label>
                    <select
                      className="form-select"
                      id="team_id"
                      name="team_id"
                      value={formData.team_id}
                      onChange={handleInputChange}
                    >
                      <option value="">No Team</option>
                      {teams.map(team => (
                        <option key={team.id} value={team.id}>
                          {team.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </form>
              </div>
              <div className="modal-footer">
                <button 
                  type="button" 
                  className="btn btn-secondary" 
                  onClick={handleCloseModal}
                  disabled={saving}
                >
                  Cancel
                </button>
                <button 
                  type="button" 
                  className="btn btn-primary" 
                  onClick={handleSave}
                  disabled={saving}
                >
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
