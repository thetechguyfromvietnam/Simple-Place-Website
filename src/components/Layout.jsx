import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu as MenuIcon, X, ShoppingCart } from 'lucide-react'
import { motion } from 'framer-motion'
import { useCart } from '../contexts/CartContext'
import DebugInfo from './DebugInfo'
import FloatingCartButton from './FloatingCartButton'

const Layout = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const location = useLocation()
  const { getTotalItems } = useCart()

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Menu', href: '/menu' },
    { name: 'About', href: '/about' },
    { name: 'Contact', href: '/contact' },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <div className="min-h-screen bg-neutral-50 overflow-x-hidden">
      {/* Navigation */}
      <header className="sticky top-0 z-30 bg-white/80 backdrop-blur border-b">
        <nav className="mx-auto max-w-6xl px-4 md:px-8 lg:px-12 h-16 flex items-center justify-between">
          <Link 
            to="/" 
            className="font-semibold text-base sm:text-lg tracking-tight flex items-center gap-2 hover:scale-105 transition-transform duration-300 flex-shrink-0"
            aria-label="Simple Place home"
          >
            <span className="inline-block h-3 w-3 rounded-full bg-amber-500 animate-float"></span>
            <span className="hidden xs:inline">Simple Place</span>
            <span className="xs:hidden">SP</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6 text-sm">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`nav-link hover:opacity-80 ${
                  isActive(item.href) ? 'text-amber-600' : 'text-neutral-700'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Action Buttons */}
          <div className="hidden md:flex items-center gap-2">
            <Link 
              to="/menu"
              className="btn-enhanced rounded-2xl px-3 lg:px-4 py-2 lg:py-3 text-xs lg:text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600"
            >
              <span className="hidden lg:inline">View Menu</span>
              <span className="lg:hidden">Menu</span>
            </Link>
            <Link 
              to="/cart"
              className="btn-enhanced rounded-2xl px-3 lg:px-4 py-2 lg:py-3 text-xs lg:text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50 relative overflow-visible"
            >
              <ShoppingCart size={14} className="inline lg:w-4 lg:h-4" />
              <span className="hidden lg:inline ml-1">Cart</span>
              {getTotalItems() > 0 && (
                <span className="absolute -top-1 -right-1 lg:-top-2 lg:-right-2 bg-red-500 text-white text-xs font-bold rounded-full min-w-[16px] lg:min-w-[18px] h-[16px] lg:h-[18px] flex items-center justify-center px-1 shadow-lg border-2 border-white">
                  {getTotalItems()}
                </span>
              )}
            </Link>
            <Link 
              to="/booking"
              className="btn-enhanced rounded-2xl px-3 lg:px-4 py-2 lg:py-3 text-xs lg:text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50"
            >
              <span className="hidden lg:inline">Book Table</span>
              <span className="lg:hidden">Book</span>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden inline-flex items-center justify-center h-10 w-10 rounded-xl border text-neutral-700 hover:bg-amber-50 transition-colors"
            aria-expanded={isMobileMenuOpen}
            aria-controls="mobileMenu"
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? <X size={20} /> : <MenuIcon size={20} />}
          </button>
        </nav>

        {/* Mobile Menu Panel */}
        {isMobileMenuOpen && (
          <motion.div 
            id="mobileMenu"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t bg-white/95 backdrop-blur"
          >
            <div className="mx-auto max-w-6xl px-4 py-3 flex flex-col gap-3 text-sm">
              {navigation.map((item, index) => (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className={`mobile-menu-item py-2 hover:text-amber-600 transition-colors ${
                    isActive(item.href) ? 'text-amber-600' : 'text-neutral-700'
                  }`}
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  {item.name}
                </Link>
              ))}
              <div className="flex flex-col gap-3 pt-4">
                <Link 
                  to="/menu"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="btn-enhanced rounded-2xl px-4 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600 text-center w-full"
                >
                  📋 Menu
                </Link>
                <Link 
                  to="/cart"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="btn-enhanced rounded-2xl px-4 py-3 text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50 text-center relative overflow-visible w-full"
                >
                  <ShoppingCart size={16} className="inline mr-2" />
                  Cart ({getTotalItems()})
                  {getTotalItems() > 0 && (
                    <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full min-w-[20px] h-[20px] flex items-center justify-center px-1 shadow-lg border-2 border-white">
                      {getTotalItems()}
                    </span>
                  )}
                </Link>
                <Link 
                  to="/booking"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="btn-enhanced rounded-2xl px-4 py-3 text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50 text-center w-full"
                >
                  📅 Book Table
                </Link>
              </div>
            </div>
          </motion.div>
        )}
      </header>

      {/* Main Content */}
      <main>
        {children}
      </main>

      {/* Footer - Hidden on Home page */}
      {location.pathname !== '/' && (
        <footer className="border-t bg-gradient-to-r from-amber-50 to-yellow-50">
          <div className="mx-auto max-w-6xl px-4 md:px-8 lg:px-12 py-10 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="text-sm text-neutral-600">
              © {new Date().getFullYear()} Simple Place. All rights reserved.
            </div>
            <div className="flex gap-4 text-sm text-neutral-600">
              {navigation.slice(1).map((item) => (
                <Link 
                  key={item.name}
                  to={item.href}
                  className="hover:text-amber-600 transition-colors"
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        </footer>
      )}
      <FloatingCartButton />
      <DebugInfo />
    </div>
  )
}

export default Layout
