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
    <div className="products-page">
        <h1>Products</h1>

        <div className="filter-row">
            <label htmlFor='category'>Filter by category:</label>
            <select
                id="Category"
                value={selectedCategory ?? ''}
                onChange={(e) => {
                    const value = e.target.value
                    setSelectedCategory(value ? Number(value) : null)
                }}
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
        {error && <div className="error">{error}</div>}

        {!loading && !error && (
            <>
                {products.length === 0 ? (
                    <p>No products found</p>
                ) : (
                    <div className="product-grid">
                        {products.map((product) => (
                            <div 
                                key={product.product_id}
                                className="product-card"
                                style={{background: product.out_of_stock ? '#fff5f5' : undefined}}
                            >
                                <h3>{product.name}</h3>
                                <p className="brand">{product.brand}</p>
                                <p className="price">${product.price.toFixed(2)}</p>
                                <p className="stock">
                                    Stock: {product.stock_quantity}
                                    {product.low_stock && (
                                        <span className="badge low">Low stock</span>
                                    )}
                                    {product.out_of_stock && (
                                        <span className="badge out">Out of Stock</span>
                                    )}
                                </p>
                                {product.category_name && (
                                    <p className="meta">Category: {product.category_name}</p>
                                )}
                                {product.size && (
                                    <p className="meta">Size: {product.size}</p>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </>
        )}
    </div>
)}
