import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Products from './Products'

function Home() {
  return(
    <div>
      <h1>SwimShop</h1>
      <p>Home Page</p>
      <Link to="/products">Products</Link>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
    <nav style={{padding:'1rem', borderBottom: '1px solid #ccc'}}>
      <Link to="/" style={{ marginRight: '1rem'}}>Home</Link>
      <Link to="/products">Products</Link>
    </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)