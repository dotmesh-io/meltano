---
sidebar: auto
metaTitle: Load Data into a Postgres with Meltano
description: Use Meltano to load data from numerous sources and insert it into a Postgres database for easy analysis.
---

# PostgreSQL Database

`target-postgres` is a loader that moves data into a PostgreSQL (same as Postgres) database. In order to use this target, you will need a Postgres database where Meltano can load data.

## Tutorials

### Beginner: Using a PostgreSQL Database for the First Time

In this section, we provide a tutorial for installing Postgres and setting up a new Postgres database.

#### Install PostgreSQL locally

1. Launch your terminal
1. Follow the [installation instructions from PostgreSQL.org](https://www.postgresql.org/download/macosx/)

#### Create Your Database

1. [Start your PostgreSQL server](https://tableplus.io/blog/2018/10/how-to-start-stop-restart-postgresql-server.html)
1. Create your first database by running `createdb <DATABASE_NAME>`
1. Connect to your postgres with the command: `psql <DATABASE_NAME>`

#### Create Your User

1. Run `createuser -s postgres` - this fixes the error: role "postgres" does not exist
1. Run `ALTER USER postgres WITH PASSWORD 'password';` with the new password of your choice
1. Run `\du` to get a list of users (from within psql)

#### Install pgAdmin

1. Go to the pgAdmin website and download the GUI https://www.pgadmin.org/
1. Install the .dmg packge that is appropriate for your operating system
1. Run the pgAdmin application and follow the prompt to create a master password
1. Back on the command line, log into your postgres user with `psql -U postgres` (by default, Postgres will log you into your username account on your machine so you will need to switch to the new user we created in the steps above)
1. Navigate to pgAdmin in your browser (it will launch a new tab when the server starts at a URL similar to http://127.0.0.1:52991/browser/#
1. On the left hand navigation bar, you should see your database listed under servers. If you don't, click "Add Server" to connect your database to pgAdmin.

![Meltano UI pipeline select PostgreSQL loader](/screenshots/pgadmin-starter-screen.png)

### Intermediate: Connecting Meltano to an Existing PostgreSQL Database

Once you have identified a PostgreSQL database where Meltano should load the data it extracts from your source(s), go to Meltano UI and complete Step 3 of the pipeline creation process.

![Meltano UI pipeline select PostgreSQL loader](/screenshots/meltano-ui-load-postgres.png)

Fill in the configuration fields with the necessary information to connect with your PostgreSQL database and click "Save". The Schema field is optional.

![Meltano UI configuring the Postgres loader](/screenshots/meltano-postgres-loader-config.png)

### Advanced: Command Line (CLI) Configuration

In this section we provide additional information for configuring Meltano to connect with your PostgreSQL databae from the Meltano command line interface (CLI).

1. Open your project's `.env` file in a text editor
1. Add the following variables to your file:

```bash
export PG_ADDRESS=""
export PG_USERNAME=""
export PG_PORT=""
export PG_PASSWORD=""
export PG_DATABASE=""
export PG_SCHEMA=""
```

## Contributor Info

- **Data Warehouse**: [Postgres](https://www.postgresql.org/)
- **Repository**: [https://github.com/meltano/target-postgres](https://github.com/meltano/target-postgres)
