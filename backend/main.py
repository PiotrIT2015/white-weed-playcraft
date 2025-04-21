import sys # Needed for executable path
import subprocess # To run the game in a separate process
import os
from fastapi import FastAPI, HTTPException
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from contextlib import contextmanager # For database connection management

# --- Configuration ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root", # Consider using environment variables for credentials
    "passwd": "12345", # Consider using environment variables for credentials
    "database": "mydb"
}

GAME_SCRIPT_PATH = os.path.join("game", "game_logic.py") # Adjust path as needed

# --- Database Connection Management ---
# Basic connection context manager (Consider a proper pool for production)
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn # Provide the connection to the endpoint
        conn.commit() # Commit changes if any (depends on usage)
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()

		# Linia 31
	# Jakiś kod powyżej...
	#finally:
		# Upewnij się, że 'finally:' jest na odpowiednim poziomie wcięcia

		# Linia 31 (wcięta względem 'finally')
		#if conn:
			# Linia 32 - POPRAWNIE! Wcięta względem 'if conn:' (np. 4 dodatkowe spacje)
		#	conn.rollback()

    # Przykład kodu zamykającego (jeśli istnieje)
    # Ta linia 'if' jest na tym samym poziomie co 'if conn:' (wcięta względem 'finally')
    if conn and conn.is_connected():
        # Ta linia 'conn.close()' jest wcięta względem 'if ... is_connected()'
        conn.close()
        # print("Database connection closed.") # Jeśli masz print, też go wciąć

# --- FastAPI App ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Endpoints ---
@app.get("/")
def root():
    # Example using the database connection
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();") # Example query
            db_name = cursor.fetchone()
            cursor.close()
            return {"message": "Hello World", "database": db_name[0] if db_name else "N/A"}
    except HTTPException as http_exc:
        # Let HTTPException pass through
        raise http_exc
    except Exception as e:
        # Catch other potential errors during DB interaction
        print(f"Error in root endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Changed to POST as it initiates an action
@app.post('/run-engine')
async def run_engine():
    """
    Launches the Pygame application in a separate process.
    """
    print("Received request to run game engine...")
    try:
        # Ensure the script exists
        if not os.path.exists(GAME_SCRIPT_PATH):
             print(f"Error: Game script not found at {GAME_SCRIPT_PATH}")
             raise HTTPException(status_code=500, detail=f"Game script not found at {GAME_SCRIPT_PATH}")

        # Launch the game script using the same Python interpreter
        # Use Popen for non-blocking execution
        process = subprocess.Popen([sys.executable, GAME_SCRIPT_PATH])

        print(f"Game process started with PID: {process.pid}")
        # Return immediately, don't wait for the game to finish
        return {"message": "Game process started successfully", "pid": process.pid}

    except Exception as e:
        print(f"\nError launching game process: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to start game process: {e}")

# Note: Pygame itself is not directly used in the FastAPI part anymore.
# It's isolated in the separate script (game/game_runner.py).

if __name__ == "__main__":
    import uvicorn
    # Ensure the game script path is correct relative to where you run uvicorn
    print(f"Checking for game script at: {os.path.abspath(GAME_SCRIPT_PATH)}")
    if not os.path.exists(GAME_SCRIPT_PATH):
         print(f"WARNING: Game script not found. The /run-engine endpoint will fail.")

    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000) # Example: Run on port 8000