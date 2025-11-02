import { Routes, Route } from 'react-router-dom'
import { CartProvider } from './contexts/CartContext'
import Layout from './components/Layout'
import Home from './pages/Home'
import Menu from './pages/Menu'
import Booking from './pages/Booking'
import Cart from './pages/Cart'
import About from './pages/About'
import Contact from './pages/Contact'

function App() {
  return (
    <CartProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/menu" element={<Menu />} />
          <Route path="/booking" element={<Booking />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </Layout>
    </CartProvider>
  )
}

export default App
