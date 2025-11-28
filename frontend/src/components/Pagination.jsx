function Pagination({ currentPage, totalPages, onPageChange }) {
    if (totalPages <= 1) return null;
  
    return (
      <div className="flex justify-center mt-8 space-x-2">
        {Array.from({ length: totalPages }, (_, index) => (
          <button
            key={index}
            onClick={() => onPageChange(index + 1)}
            className={`px-4 py-2 rounded-md border text-sm font-medium transition-colors
              ${
                currentPage === index + 1
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 border-gray-400 hover:bg-gray-300 dark:hover:bg-gray-600"
              }`}
          >
            {index + 1}
          </button>
        ))}
      </div>
    );
  }
  
  export default Pagination;
  