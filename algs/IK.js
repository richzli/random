/*
 * IK.js
 *
 * two-joint 2D rigidbody inverse kinematics for use in after
 *   effects expressions
 */

/* 
 * JOINT 2 should be parented to JOINT 1
 * JOINT 3 should *NOT* be parented to JOINT 2
 */
var j1 = thisComp.layer("JOINT 1")
var j2 = thisComp.layer("JOINT 2")
var j3 = thisComp.layer("JOINT 3")

var z = j1.parent // if joint 1 has no parent then set to a null object w/ no transforms

/*
 * assuming the layers are the same size as the composition
 *   and no initial transforms, which means that anchor
 *   points are in world coordinates
 * 
 * if this isn't the case, then hard-code the initial coords here
 */
var A = j1.transform.anchorPoint
var B = j2.transform.anchorPoint
var C = j3.transform.anchorPoint

/*
 * joint 3 (point C) moves freely; joint 1 (point A) is parented
 *   to something else (which ostensibly is moving around in
 *   some linked motion)
 * 
 * A' (== A$) and C' are the current position of the anchor points
 *   (as opposed to the initial positions)
 */
var A$ = j1.toWorld(A)
var C$ = j3.toWorld(C)

/*
 * calculate the lengths of relevant segments
 */
function dist(v) {
    return Math.sqrt(v[0] * v[0] + v[1] * v[1])
}

var AB = dist(B - A)
var BC = dist(C - B)
var A$C$ = dist(C$ - A$)

/*
 * calculate the angles of these segments w.r.t the horizontal
 */
function angle(start, end) {
    return Math.atan2(end[1] - start[1], end[0] - start[0]);
}

var aAB = angle(A, B)
var aBC = angle(B, C)

/*
 * calculate the position of B' using these lengths and angles
 */
function cross(v1, v2) {
    return v1[0] * v2[1] - v2[0] * v1[1]
}
function sgn_nz(x) {
    return x == Math.abs(x) ? 1 : -1;
}
function clamp(x, mn, mx) {
    return Math.min(Math.max(x, mn), mx)
}

var aA$ = Math.acos(clamp((A$C$ * A$C$ + AB * AB - BC * BC) / (2 * A$C$ * AB), -1, 1))
var aA$C$ = angle(A$, C$)

var flip = false // if the joint is going the wrong way, toggle this

var B$ = A$ + [AB * Math.cos(aA$C$ + aA$), AB * Math.sin(aA$C$ + aA$)]
var B$2 = A$ + [AB * Math.cos(aA$C$ - aA$), AB * Math.sin(aA$C$ - aA$)]

if ((sgn_nz(cross(C - A, B - A)) != sgn_nz(cross(C$ - A$, B$ - A$))) ^ flip) {
    B$ = B$2
}

/*
 * calculate necessary rotations to be applied to each joint
 */

var aA$B$ = angle(A$, B$)
var aB$C$ = angle(B$, C$)


/*
 * these values are in radians, so convert to degrees if using directly
 *
 * `transform.rotation + rot_jX * 180 / Math.PI`
 */
var rot_j1 = -aAB - angle([0, 0], z.fromWorldVec([1, 0])) + aA$B$
var rot_j2 = -aBC - rot_j1 + aB$C$
var rot_j3 = -rot_j2 - rot_j1 // + your motion of choice