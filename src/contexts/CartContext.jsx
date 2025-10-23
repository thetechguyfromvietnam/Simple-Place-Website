import React, { createContext, useContext, useReducer, useEffect } from 'react'

const CartContext = createContext()

const cartReducer = (state, action) => {
  switch (action.type) {
    case 'ADD_ITEM':
      const existingItem = state.items.find(item => item.id === action.payload.id)
      if (existingItem) {
        return {
          ...state,
          items: state.items.map(item =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + action.payload.quantity }
              : item
          )
        }
      }
      return {
        ...state,
        items: [...state.items, { ...action.payload, quantity: action.payload.quantity || 1 }]
      }

    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload)
      }

    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: Math.max(0, action.payload.quantity) }
            : item
        ).filter(item => item.quantity > 0)
      }

    case 'CLEAR_CART':
      return {
        ...state,
        items: []
      }

    case 'LOAD_CART':
      return {
        ...state,
        items: action.payload || []
      }

    default:
      return state
  }
}

export const CartProvider = ({ children }) => {
  const [state, dispatch] = useReducer(cartReducer, { items: [] })

  // Load cart from localStorage on mount
  useEffect(() => {
    const savedCart = localStorage.getItem('simple-place-cart')
    if (savedCart) {
      try {
        dispatch({ type: 'LOAD_CART', payload: JSON.parse(savedCart) })
      } catch (error) {
        console.error('Error loading cart from localStorage:', error)
      }
    }
  }, [])

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('simple-place-cart', JSON.stringify(state.items))
  }, [state.items])

  const addToCart = (item, quantity = 1) => {
    // Create unique ID that includes size for pizza items and taco options
    let uniqueId = item.name
    if (item.size) uniqueId += `-${item.size}`
    if (item.tacoOption) uniqueId += `-${item.tacoOption}`
    uniqueId += `-${item.price}`
    
    const cartItem = {
      id: uniqueId,
      name: item.name,
      price: item.price,
      unit: item.unit,
      image: item.image,
      size: item.size, // Include size information
      tacoOption: item.tacoOption, // Include taco option information
      quantity
    }
    dispatch({ type: 'ADD_ITEM', payload: cartItem })
  }

  const removeFromCart = (itemId) => {
    dispatch({ type: 'REMOVE_ITEM', payload: itemId })
  }

  const updateQuantity = (itemId, quantity) => {
    dispatch({ type: 'UPDATE_QUANTITY', payload: { id: itemId, quantity } })
  }

  const clearCart = () => {
    dispatch({ type: 'CLEAR_CART' })
  }

  const getTotalPrice = () => {
    return state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
  }

  const getTotalItems = () => {
    return state.items.reduce((total, item) => total + item.quantity, 0)
  }

  // VAT calculation functions
  const isAlcoholItem = (item) => {
    const name = item.name.toLowerCase()
    return name.includes('bia') || name.includes('beer') || name.includes('wine') || 
           name.includes('cocktail') || name.includes('spirit') || name.includes('liquor')
  }

  const getFoodSubtotal = () => {
    return state.items
      .filter(item => !isAlcoholItem(item))
      .reduce((total, item) => total + (item.price * item.quantity), 0)
  }

  const getAlcoholSubtotal = () => {
    return state.items
      .filter(item => isAlcoholItem(item))
      .reduce((total, item) => total + (item.price * item.quantity), 0)
  }

  const getFoodVAT = () => {
    return Math.round(getFoodSubtotal() * 0.08)
  }

  const getAlcoholVAT = () => {
    return Math.round(getAlcoholSubtotal() * 0.10)
  }

  const getTotalVAT = () => {
    return getFoodVAT() + getAlcoholVAT()
  }

  const getTotalWithVAT = () => {
    return getTotalPrice() + getTotalVAT()
  }

  const value = {
    items: state.items,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    getTotalPrice,
    getTotalItems,
    // VAT functions
    isAlcoholItem,
    getFoodSubtotal,
    getAlcoholSubtotal,
    getFoodVAT,
    getAlcoholVAT,
    getTotalVAT,
    getTotalWithVAT
  }

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  )
}

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}
