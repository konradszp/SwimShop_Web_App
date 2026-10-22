import { useEffect, useState } from 'react'
import axios from 'axios'

type Product = {
    product_id: number
    category_id: number
    category_name: string | null
    name: string
    brand: string
    price: number
    stock_quantity: number
    min_stock_level: number | null
    size: string | null
    description: string | null
    low_stock: boolean
    out_of_stock: boolean
}

type Category = {
    category_id: number
    name: string
}

export default function Products() {
    const [products, setProducts] = useState<Product[]>([])
    const [categories, setCategories] = useState<Category[]>([])
    const [selectedCategory, setSelectedCategory] = useState<number | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        axios
            .get<Category[]>('http://localhost:8000/categories')
            .then((res) => setCategories(res.data))
            .catch((err) => console.error('Failed to load categories', err))
    }, [])

    useEffect(() => {
        setLoading(true)
        setError(null)

        const url = selectedCategory
        ? `http://localhost:8000/products/category/${selectedCategory}`
        : 'http://localhost:8000/products'

        axios
            .get<Product[]>(url)
            .then((res) => {
                setProducts(res.data)
                setLoading(false)
        })
        .catch((err) => {
            console.error(err)
            setError('Failed to load products')
            setLoading(false)
        })
    }, [selectedCategory])

return (
    <div style={{ padding: '2rem'}}>
        <h1>Products</h1>

        <div style={{marginBottom: '2rem'}}>
            <label htmlFor='category' style={{marginRight: '1rem'}}>
                Filter by category:
            </label>
            <select
                id="Category"
                value={selectedCategory ?? ''}
                onChange={(e) => {
                    const value = e.target.value
                    setSelectedCategory(value ? Number(value) : null)
                }}
                style={{padding: '0.5rem 0.7rem'}}
                >
                    <option value="">All categories</option>
                    {categories.map((cat) => (
                        <option key={cat.category_id} value={cat.category_id}>
                            {cat.name}
                        </option>
                    ))}
            </select>
        </div>

        {loading && <div>Loading products...</div>}
        {error && <div style={{ color: 'red'}}>{error}</div>}

        {!loading && !error && (
            <>
                {products.length === 0 ? (
                    <p>No products found</p>
                ) : (
                    <div style={{
                        display: 'grid',
                        gap: '1rem',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))'
                    }}>
                        {products.map((product) => (
                            <div key={product.product_id} style={{
                                border: '1px solid #ddd',
                                borderRadius: '10px',
                                padding: '1rem',
                                background: product.out_of_stock ? '#fff5f5' : 'fff',
                            }}>
                            <h3 style={{margin: '0 0 0.5rem'}}>{product.name}</h3>
                            <p style={{margin:'0.25rem 0', color: '#555'}}>{product.brand}</p>
                            <p style={{margin: '0.25rem 0'}}>
                                <strong>${product.price.toFixed(2)}</strong>
                            </p>
                            <p style={{margin: '0.25rem 0', fontSize: '1rem'}}>
                                Stock: {product.stock_quantity}
                                {product.low_stock && (
                                    <span style={{color: 'orange', marginLeft: '0.5rem'}}>Low stock</span>
                                )}
                                {product.out_of_stock && (
                                    <span style={{color: 'red', marginLeft: '0.5rem'}}>Out of Stock</span>
                                )}
                            </p>
                            {product.category_name && (
                                <p style={{margin: '0.25rem 0', fontSize: '1rem', color: '#777'}}>
                                    Category: {product.category_name}
                                </p>
                            )}
                            {product.size && (
                                <p style={{ margin: '0.25rem 0', fontSize: '1rem'}}>Size: {product.size}</p>
                            )}
                            </div>
                        ))}
                    </div>
                )}
            </>
        )}
    </div>
)}
