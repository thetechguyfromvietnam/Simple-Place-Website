import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { X } from 'lucide-react'

const TacoOptionsSelector = ({ item, onAddToCart, onClose }) => {
  const [selectedOption, setSelectedOption] = useState('Crispy')
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price)
  }

  const handleAddToCart = () => {
    const cartItem = {
      ...item,
      name: `${item.name} (${selectedOption})`,
      tacoOption: selectedOption
    }
    onAddToCart(cartItem)
    onClose()
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        className="bg-white rounded-2xl max-w-md w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-900">Choose Taco Style</h2>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors"
          >
            <X size={16} />
          </button>
        </div>

        {/* Taco Info */}
        <div className="p-6 border-b border-gray-100">
          <img
            src={item.image}
            alt={item.name}
            className="w-full h-48 object-cover rounded-xl mb-4"
          />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.name}</h3>
          <p className="text-gray-600 text-sm">Choose your preferred taco style (free option)</p>
        </div>

        {/* Style Options */}
        <div className="p-6 space-y-4">
          {/* Crispy Taco */}
          <div
            className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
              selectedOption === 'Crispy'
                ? 'border-amber-500 bg-amber-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => setSelectedOption('Crispy')}
          >
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-semibold text-gray-900">Crispy</h4>
                <p className="text-sm text-gray-600">Traditional crispy corn shell</p>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-gray-900">FREE</p>
              </div>
            </div>
          </div>

          {/* Soft Taco */}
          <div
            className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
              selectedOption === 'Soft'
                ? 'border-amber-500 bg-amber-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => setSelectedOption('Soft')}
          >
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-semibold text-gray-900">Soft</h4>
                <p className="text-sm text-gray-600">Soft flour tortilla</p>
                <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full mt-1">
                  Popular Choice
                </span>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-gray-900">FREE</p>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="p-6 border-t border-gray-100 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 py-3 px-4 border border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleAddToCart}
            className="flex-1 py-3 px-4 bg-amber-500 text-white rounded-xl font-semibold hover:bg-amber-600 transition-colors"
          >
            Add to Cart - {formatPrice(item.price)}
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}

export default TacoOptionsSelector
