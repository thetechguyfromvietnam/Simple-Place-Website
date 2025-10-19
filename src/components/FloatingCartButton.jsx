import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { ShoppingCart, X } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useCart } from '../contexts/CartContext'

const FloatingCartButton = () => {
  const { getTotalItems, items, getTotalPrice, removeFromCart } = useCart()
  const [isHovered, setIsHovered] = useState(false)

  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price)
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 1, type: "spring", stiffness: 200 }}
      className="fixed bottom-4 right-4 md:bottom-6 md:right-6 z-50"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Cart Preview Popup */}
      {isHovered && items.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 20, scale: 0.8 }}
          className="absolute bottom-20 right-0 w-72 md:w-80 bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden"
        >
          <div className="p-4 border-b border-gray-100">
            <h3 className="font-semibold text-gray-900">Cart Preview</h3>
            <p className="text-sm text-gray-600">{getTotalItems()} items</p>
          </div>
          
          <div className="max-h-64 overflow-y-auto">
            {items.slice(0, 3).map((item) => (
              <div key={item.id} className="flex items-center gap-3 p-3 border-b border-gray-50">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-12 h-12 object-cover rounded-lg"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 text-sm truncate">{item.name}</p>
                  <p className="text-xs text-gray-600">Qty: {item.quantity}</p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900 text-sm">{formatPrice(item.price * item.quantity)}</p>
                  <button
                    onClick={(e) => {
                      e.preventDefault()
                      removeFromCart(item.id)
                    }}
                    className="text-red-500 hover:text-red-700 text-xs"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
            {items.length > 3 && (
              <div className="p-3 text-center text-sm text-gray-600">
                +{items.length - 3} more items
              </div>
            )}
          </div>
          
          <div className="p-4 bg-gray-50 border-t border-gray-100">
            <div className="flex justify-between items-center mb-3">
              <span className="font-semibold text-gray-900">Total:</span>
              <span className="font-bold text-amber-600">{formatPrice(getTotalPrice())}</span>
            </div>
            <Link
              to="/cart"
              className="w-full bg-amber-500 hover:bg-amber-600 text-white py-2 px-4 rounded-lg font-semibold text-sm transition-colors duration-200 text-center block"
            >
              View Cart & Checkout
            </Link>
          </div>
        </motion.div>
      )}

      <Link
        to="/cart"
        className="group relative"
      >
        {/* Main Cart Button */}
        <motion.div
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          className="w-14 h-14 md:w-16 md:h-16 bg-amber-500 hover:bg-amber-600 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 cursor-pointer"
        >
          <ShoppingCart size={20} className="text-white md:w-6 md:h-6" />
          
          {/* Cart Badge */}
          {getTotalItems() > 0 && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 500 }}
              className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full min-w-[24px] h-[24px] flex items-center justify-center px-1 shadow-lg border-2 border-white"
            >
              {getTotalItems()}
            </motion.div>
          )}
        </motion.div>

        {/* Tooltip */}
        <div className="absolute bottom-full right-0 mb-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
          <div className="bg-gray-900 text-white text-sm px-3 py-2 rounded-lg whitespace-nowrap">
            {getTotalItems() > 0 ? `View Cart (${getTotalItems()} items)` : 'View Cart'}
            <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
          </div>
        </div>

        {/* Pulse Animation when cart has items */}
        {getTotalItems() > 0 && (
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="absolute inset-0 bg-amber-400 rounded-full opacity-30"
          />
        )}
      </Link>
    </motion.div>
  )
}

export default FloatingCartButton
