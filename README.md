Let me clear this is hosted as a reference of the project for my own benefit, and is not intended for use by anyone else (though, you can if you really want). Various key, personal elements have been removed or altered to be posted onto github and it would require modification to be used by someone else.

Discord.py is required to be installed to run the project
Have all files in the same shared file/directory
Open `Economy Bot MAIN.py` and run it

The various public tweaks would need to be reversed, and a Discord API token provided at the bottom of `Economy Bot MAIN.py`.

The MAIN file (`Economy Bot MAIN.py`) imports the sub-files and references their functions/classes. The user's message is lowercased and passed down the logic until it befits the called sub-file (so someone typing "-rob" only triggers the code in the `Rob.py` file). This helps with easily modifying the different features and it not affecting other core pieces of the project.

`Asyncio_Scheduler.py` is an important file that handles time cycles, such as updating the database every 24 hours at a certain time, or messaging users their stock updates on a weekly basis at certain times.

The data is stored within an SQL database. The current uploaded file is the database as I had it at the time of upload, but with personal information removed.
