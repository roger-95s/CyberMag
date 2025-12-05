function Pagination({ currentPage, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  const isFirst = currentPage === 1;
  const isLast = currentPage === totalPages;

  const baseBtn =
    "px-3 py-2 rounded-md border text-sm font-medium transition-colors";
  const activeBtn = "bg-blue-600 text-white border-blue-600";
  const inactiveBtn =
    "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 border-gray-400 hover:bg-gray-300 dark:hover:bg-gray-600";
  const disabledBtn =
    "bg-gray-100 dark:bg-gray-800 text-gray-400 border-gray-300 cursor-not-allowed";

  return (
    <div className="flex justify-center mt-8 space-x-2">
      {/* go to first*/}
      <button
        onClick={() => onPageChange(1)}
        disabled={isFirst}
        className={`${baseBtn} ${isFirst ? disabledBtn : inactiveBtn}`}
      >
        «
      </button>

      {/* after */}
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={isFirst}
        className={`${baseBtn} ${isFirst ? disabledBtn : inactiveBtn}`}
      >
        ‹
      </button>

      {/* numbers */}
      {Array.from({ length: totalPages }, (_, index) => {
        const page = index + 1;
        const isActive = currentPage === page;

        return (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            className={`${baseBtn} ${isActive ? activeBtn : inactiveBtn}`}
          >
            {page}
          </button>
        );
      })}

      {/* Next  */}
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={isLast}
        className={`${baseBtn} ${isLast ? disabledBtn : inactiveBtn}`}
      >
        ›
      </button>

      {/* go to the last */}
      <button
        onClick={() => onPageChange(totalPages)}
        disabled={isLast}
        className={`${baseBtn} ${isLast ? disabledBtn : inactiveBtn}`}
      >
        »
      </button>
    </div>
  );
}

export default Pagination;
