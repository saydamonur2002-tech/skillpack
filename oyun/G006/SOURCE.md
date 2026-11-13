# Source and changes: NPC steering behaviours: seek, flee, arrive, pursuit (Yuka)

Upstream: https://github.com/Mugen87/yuka at commit `10591304811222d6856020d5de129b39ef43b58d` (0.7.8), license MIT.

## What was taken

SeekBehavior, FleeBehavior, ArriveBehavior, PursuitBehavior, SteeringManager._accumulate and Vehicle.update integration

## Port notes

2D port of Yuka's 3D vector maths on the x-z plane (Yuka y=0). Direction (getDirection) is modelled as the normalised last displacement, which is what Vehicle.update sets through lookAt when speed^2 > 1e-8; before any movement it is the given heading, the velocity direction, or Yuka's forward +z. A single behaviour with weight 1 passes through SteeringManager._accumulate. Smoother is not used (Yuka default null).

## Evidence and exact source pins

- [src/constants.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/constants.js) — complete original file; SHA-256 `f2c832d90c29d85263af0158d71b1480151fb0d809fab9b1ac08aa265e7afbf0`.
- [src/core/GameEntity.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/core/GameEntity.js) — complete original file; SHA-256 `ab5c9b73762013bb164bc7c690a7b34fb95ad60a9e604ed6becdc05442271eea`.
- [src/core/Logger.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/core/Logger.js) — complete original file; SHA-256 `baaa5dfc332f7faa2f80df0658fcc0d2307ea1e82890a225a83d646a0379c523`.
- [src/core/MovingEntity.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/core/MovingEntity.js) — complete original file; SHA-256 `2914f33242918b765f1b073363deabf7431c4a4d151fbf159ea78e7e059e15bb`.
- [src/math/AABB.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/math/AABB.js) — complete original file; SHA-256 `9a8cea58e4b2e4fb890d482cf32d273b393225694842dac24bec4617acc156e3`.
- [src/math/BoundingSphere.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/math/BoundingSphere.js) — complete original file; SHA-256 `eaead44120e57b3317f0e61e4d8d5ba002db448c6a7307234caf03a764ba7639`.
- [src/math/MathUtils.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/math/MathUtils.js) — complete original file; SHA-256 `637a05b236646f09d4bcfae3beca42db5f716bdfd0600fe5ff0596b15a6469db`.
- [src/math/Matrix3.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/math/Matrix3.js) — complete original file; SHA-256 `6bb656b574041502f9430967de884b2fac015459bb32033e3b8cd59f3fec8a67`.
- [src/math/Matrix4.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/math/Matrix4.js) — complete original file; SHA-256 `83045b6af86180ad70d27199eeb6fd9b5659a4fe24e94b807510813bc626203a`.
- [src/math/Quaternion.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/math/Quaternion.js) — complete original file; SHA-256 `59d16f0cda03c81951eb3ae6b3e6b1ca34036c6853c351e26fa4e5be3bb00c84`.
- [src/math/Ray.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/math/Ray.js) — complete original file; SHA-256 `3877ac3450e363111d3bc23860f90a87417f46616503efa5dbc3a1e22b5e3b1b`.
- [src/math/Vector3.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/math/Vector3.js) — complete original file; SHA-256 `133eacf2a34219af539d0e2569be6a7eb890b0df4c9aab3cc01a1433a3458cf3`.
- [src/steering/Path.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/Path.js) — complete original file; SHA-256 `be82c7044d09fd95d0f29c628f2572993fe3187921a26cbe2bd35e374d4bf0bd`.
- [src/steering/Smoother.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/Smoother.js) — complete original file; SHA-256 `fb4a863d9a5e31af5557f485612ac55fd9322cac9384c17ae717d01123c17a13`.
- [src/steering/SteeringBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/SteeringBehavior.js) — complete original file; SHA-256 `87db1345b4514e577deb3c9ddd8a51e85bb52e3c703f8c3866eee8cb11b26b94`.
- [src/steering/SteeringManager.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/SteeringManager.js) — complete original file; SHA-256 `b91ec0cc31e20244f0c87e8bf44a03595f1b857dd4f3306874478291a8c5cba7`.
- [src/steering/Vehicle.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/Vehicle.js) — complete original file; SHA-256 `d6300be887cc7d20ce247ee4448d82e9caa02584350159dc63c5d35d104b1e28`.
- [src/steering/behaviors/AlignmentBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/AlignmentBehavior.js) — complete original file; SHA-256 `097fcf54a5dc23e0b87f01ebefeb37bf44254176ef8657628625b9bca6af8801`.
- [src/steering/behaviors/ArriveBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/ArriveBehavior.js) — complete original file; SHA-256 `c3b687534ba7f8a17f3d2991317deb419322e14a091ac77bab2b0f38aab4b31f`.
- [src/steering/behaviors/CohesionBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/CohesionBehavior.js) — complete original file; SHA-256 `9979277defd6f47530b2ebc448bb61fb6f8ad6cc0c820e09814e3c992aad7617`.
- [src/steering/behaviors/EvadeBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/EvadeBehavior.js) — complete original file; SHA-256 `21d0df214e669574ce9ac400041842421b35a60300faf72c3875ea599b42c2a3`.
- [src/steering/behaviors/FleeBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/FleeBehavior.js) — complete original file; SHA-256 `375c6b83665e1a867028d4a16076c0e6c2f38b49193f9754256e035387277456`.
- [src/steering/behaviors/FollowPathBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/FollowPathBehavior.js) — complete original file; SHA-256 `4a9624bb8e8eace7e89247bfff814787f87b4547293513b4a7ce5a7080bc0757`.
- [src/steering/behaviors/InterposeBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/InterposeBehavior.js) — complete original file; SHA-256 `c48ded0bbde36d92124ea5c7a8b603f76f3f26e0c0e990e7cf6249db9a2a505d`.
- [src/steering/behaviors/ObstacleAvoidanceBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/ObstacleAvoidanceBehavior.js) — complete original file; SHA-256 `878763d7c0158c6140d9bb1990bf550c6233b904f1da97e16268742552110973`.
- [src/steering/behaviors/OffsetPursuitBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/OffsetPursuitBehavior.js) — complete original file; SHA-256 `4f2b57bc5d093b5d30d2e1c8793d473f2a3a984effb55aba5610c871c3b5e978`.
- [src/steering/behaviors/PursuitBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/PursuitBehavior.js) — complete original file; SHA-256 `1d0d48ab5c7592440547bf968a965810dc2e233595af57b42e0658390cdce086`.
- [src/steering/behaviors/SeekBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/SeekBehavior.js) — complete original file; SHA-256 `df276769933ab59714e72640e7b770fb50df0a9697a42a12b11c318fcdc7afca`.
- [src/steering/behaviors/SeparationBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/SeparationBehavior.js) — complete original file; SHA-256 `3bef63b70cbad2363c7a9004bf3dfeae48e35ff7c1f60b45e9a503c8c1a15c92`.
- [src/steering/behaviors/WanderBehavior.js](https://github.com/Mugen87/yuka/blob/10591304811222d6856020d5de129b39ef43b58d/src/steering/behaviors/WanderBehavior.js) — complete original file; SHA-256 `820137f2e4df6339c4fe305f9daa5f4c8aefb9989922010f8a4c392843b7b81d`.

## Reference values

Every case was generated by executing the pinned Yuka src/ modules (Vehicle, MovingEntity, Seek/Flee/Arrive/Pursuit behaviours) in Node.js through reference/upstream_harness.mjs.
