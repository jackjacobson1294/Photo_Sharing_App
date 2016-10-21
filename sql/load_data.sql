USE group120db;
INSERT INTO User VALUES('spacejunkie', 'Bob', 'Spacey', 'sha512$757e76b0b7164038b822d8ed3a4f450e$770d54f97c4747dd678e51002eeefd8e3f1b1d9a95dfb919f9eaa1f277577de887f297b5c759c52c9dac9fb6ac4bdf5486fd7c487d111914ef3cfc57ecd74b5d', 'bspace@spacejunkies.net');
INSERT INTO User VALUES('sportslover', 'Paul', 'Walker', 'sha512$d0a471f213744c0191f81684b9070561$eaac364726bff20ce1045a5703362de4946ecfa210bee8c20eb93085c0f3bae02f994561bd5ea64f4a3d3298a246fe60f721cb2837f10bab8c2811abfae82b66', 'sportslover@hotmail.com');
INSERT INTO User VALUES('traveler', 'Rebecca', 'Travolta', 'sha512$60d060cff04a4310a7c866f2183ece0a$2d886581f4137dba5de4b8242480d6d4fd93c5bb5c5ec697048f9b981dcea0a99e68b39645e0c81d199f67d35096507d9bc4e8c3bf846b17d659129bb94cd5b8', 'rebt@explorer.org');
INSERT INTO Album VALUES(NULL,'I love sports', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), 'sportslover', 'public'), (NULL,'I love football', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), 'sportslover', 'private'), (NULL,'Around The World', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), 'traveler', 'public'), (NULL,'Cool Space Shots', CURRENT_TIMESTAMP(), NULL, 'spacejunkie', 'private');
INSERT INTO Photo VALUES('001025dd643b0eb0661e359de86e3ea9', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(0, 2, '001025dd643b0eb0661e359de86e3ea9', "");
INSERT INTO Photo VALUES('9a0a7d25af4f7a73f67dde74e8e54cff', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(1, 2, '9a0a7d25af4f7a73f67dde74e8e54cff', "");
INSERT INTO Photo VALUES('c8e60100f13ffe374d59e39dc4b6a318', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(2, 2, 'c8e60100f13ffe374d59e39dc4b6a318', "");
INSERT INTO Photo VALUES('5e8b6207f007338243d3e29d6b82acab', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(3, 2, '5e8b6207f007338243d3e29d6b82acab', "");
INSERT INTO Photo VALUES('4ddba6e2f905e9778c6b6a48b6fc8e03', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(4, 4, '4ddba6e2f905e9778c6b6a48b6fc8e03', "");
INSERT INTO Photo VALUES('09d8a979fa638125b02ae1578eb943fa', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(5, 4, '09d8a979fa638125b02ae1578eb943fa', "");
INSERT INTO Photo VALUES('143ba34cb5c7e8f12420be1b576bda1a', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(6, 4, '143ba34cb5c7e8f12420be1b576bda1a', "");
INSERT INTO Photo VALUES('e615a10fc4222ede59ca3316c3fb751c', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(7, 4, 'e615a10fc4222ede59ca3316c3fb751c', "");
INSERT INTO Photo VALUES('65fb1e2aa4977d9414d1b3a7e4a3badd', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(8, 4, '65fb1e2aa4977d9414d1b3a7e4a3badd', "");
INSERT INTO Photo VALUES('b94f256c23dec8a2c0da546849058d9e', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(9, 1, 'b94f256c23dec8a2c0da546849058d9e', "");
INSERT INTO Photo VALUES('01e37cbdd55913df563f527860b364e8', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(10, 1, '01e37cbdd55913df563f527860b364e8', "");
INSERT INTO Photo VALUES('8d554cd1d8bb7b49ca798381d1fc171b', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(11, 1, '8d554cd1d8bb7b49ca798381d1fc171b', "");
INSERT INTO Photo VALUES('2e9e69e19342b98141789925e5f87f60', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(12, 1, '2e9e69e19342b98141789925e5f87f60', "");
INSERT INTO Photo VALUES('298e8943ef1942159ef88be21c4619c9', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(13, 1, '298e8943ef1942159ef88be21c4619c9', "");
INSERT INTO Photo VALUES('cefe45eaeaeb599256dda325c2e972da', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(14, 1, 'cefe45eaeaeb599256dda325c2e972da', "");
INSERT INTO Photo VALUES('bf755d13bb78e1deb59ef66b6d5c6a70', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(15, 1, 'bf755d13bb78e1deb59ef66b6d5c6a70', "");
INSERT INTO Photo VALUES('5f8d7957874f1303d8300e50f17e46d6', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(16, 1, '5f8d7957874f1303d8300e50f17e46d6', "");
INSERT INTO Photo VALUES('bac4fca50bed35b9a5646f632bf4c2e8', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(17, 3, 'bac4fca50bed35b9a5646f632bf4c2e8', "");
INSERT INTO Photo VALUES('f5b57bd7a2c962c54d55b5ddece37158', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(18, 3, 'f5b57bd7a2c962c54d55b5ddece37158', "");
INSERT INTO Photo VALUES('b7d833dd3aae203ca618759fc6f4fc01', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(19, 3, 'b7d833dd3aae203ca618759fc6f4fc01', "");
INSERT INTO Photo VALUES('faa20c04097d40cb10793a19246f2754', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(20, 3, 'faa20c04097d40cb10793a19246f2754', "");
INSERT INTO Photo VALUES('aaaadd578c78d21defaa73e7d1f08235', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(21, 3, 'aaaadd578c78d21defaa73e7d1f08235', "");
INSERT INTO Photo VALUES('adb5c3af19664129141268feda90a275', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(22, 3, 'adb5c3af19664129141268feda90a275', "");
INSERT INTO Photo VALUES('abf97ffd1f964f42790fb358e5258e8d', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(23, 3, 'abf97ffd1f964f42790fb358e5258e8d', "");
INSERT INTO Photo VALUES('ea2db8b970671856e43dd011d7df5fad', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(24, 3, 'ea2db8b970671856e43dd011d7df5fad', "");
INSERT INTO Photo VALUES('76d79b81b9073a2323f0790965b00a68', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(25, 3, '76d79b81b9073a2323f0790965b00a68', "");
INSERT INTO Photo VALUES('6510a4add59ef655ae3f0b6cdb24e140', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(26, 3, '6510a4add59ef655ae3f0b6cdb24e140', "");
INSERT INTO Photo VALUES('28d38afca913a728b2a6bcf01aa011cd', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(27, 3, '28d38afca913a728b2a6bcf01aa011cd', "");
INSERT INTO Photo VALUES('5fb04eb11cbf99429a05c12ce2f50615', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(28, 3, '5fb04eb11cbf99429a05c12ce2f50615', "");
INSERT INTO Photo VALUES('39ee267d13ccd32b50c1de7c2ece54d6', 'jpg', CURRENT_TIMESTAMP());
INSERT INTO Contain VALUES(29, 3, '39ee267d13ccd32b50c1de7c2ece54d6', "");