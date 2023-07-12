# Matchflix-n-Chill
Introducing Matchflix-n-Chill: Uniting Film Enthusiasts Through the Power of Connection

Welcome to Matchflix-n-Chill, a dynamic web application that goes beyond the screen to foster genuine connections among movie lovers. Are you tired of watching films alone and yearn for stimulating discussions with like-minded individuals? Look no further. Matchflix-n-Chill leverages a powerful matching algorithm that brings users together based on their shared interests in various movies.

Gone are the days of solitary movie marathons. With Matchflix-n-Chill, you can broaden your social circle and forge new friendships with ease. Immerse yourself in a vibrant community where enthusiasts converge to discuss their favorite films, exchange recommendations, and ignite engaging conversations. The application enables you to connect, chat, and bond with people who share your passion for cinema.

## Install
To install all dependencies run the following command on the root
directory of this project:

```linux
make install
```

To run the app locally:

```linux
make
```
to seed the app for visual tests go to route /test when you run the app locally

## Database

![image](https://github.com/harobosan/Matchflix-n-Chill/assets/83618808/dda142d6-121a-49ee-b25e-3aa00fbd9d8b)

If you apply alterations to database schema run the following command on your local machine
```linux
make clean
```

## Main Functionalities
  - User can create an account
  - User can log in his account
  - Anyone can see a variety of movies from our catalog
  - User can like or dislike movies from our catalog
  - User can see recommendations of other users based on algorithm
  - User can send or receive friend requests
  - User can end friendships
  - User can chat with friends 

## Tests

To run all code tests:

```linux
make test
```

To run all code tests and see coverage:

```linux
make coverage
```

To run a static verifier for lint errors:

```linux
make static
```
