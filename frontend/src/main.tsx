import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function Home() {
  return(
    <div>
      <h1>SwimShop</h1>
      <p>Home Page</p>
      <Link to="/products">Products</Link>
    </div>
  )
}

function Products(){
  return(
    <div>
      <h1>Products</h1>
      <p>Products List</p>
      <Link to="/">Home</Link>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)