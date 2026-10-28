import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Products from './Products'
import './style.css'

function Home() {
  return(
    <div className="home">
      <h1>SwimShop</h1>
      <p className="subtitle">Swimming gear POS system</p>
      <div className="cards">
        <Link to="/products" className="card">
          <h3>Products</h3>
          <p>View and filter inventory</p>
        </Link>

        <div className="card disabled">
          <h3>Orders</h3>
          <p>...</p>
        </div>

        <Link to="/products" className="card">
          <h3>Low Stock</h3>
          <p>Check items that need restock</p>
        </Link>
      </div>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
    <nav className="nav">
      <Link to="/" className="nav-brand">Swimshop</Link>
      <Link to="/">Home</Link>
      <Link to="/products">Products</Link>
    </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)