import { useState} from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Login(){
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState<string|null>(null)
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)
        setLoading(true)

        try {
            const formData = new URLSearchParams()
            formData.append('username', username)
            formData.append('password', password)

            const res = await axios.post('http://localhost:8000/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            })

            localStorage.setItem('token', res.data.access_token)
            localStorage.setItem('user', JSON.stringify({
                username: res.data.username,
                full_name: res.data.full_name,
                role: res.data.role,
            }))

            navigate('/')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Login failed')
        } finally {
            setLoading(false)
        }
    }
    return (
    <div className="login-page">
        <div className="login-box">
            <h1>Swimshop Login</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                        id="username"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        autoFocus
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <div className="error">{error}</div>}
                <button type="submit" disabled={loading}>
                    {loading ? 'Loggin in...' : 'Log in'}
                </button>
            </form>
        </div>
    </div>
    )
}

