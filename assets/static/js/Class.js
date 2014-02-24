/**
 * @file Class.js
 * @author Josh Gertzan
 * @date Spring 2013
 *
 * The "Class" type describes a type that can be inherited from using
 * the 'extend' function.  This allows for polymorphism in the classical
 * sense (i.e. like object-oriented languages).
 *
 * @see http://joshgertzen.com/object-oriented-super-class-method-calling-with-javascript/
 */

function Class() { }
Class.prototype.construct = function() {};
Class.__asMethod__ = function(func, superClass) {
    return function() {
        var currentSuperClass = this._$;
        this._$ = superClass;
        var ret = func.apply(this, arguments);
        this._$ = currentSuperClass;
        return ret;
    };
};

Class.extend = function(def) {
    var classDef = function() {
        if (arguments[0] !== Class) { this.construct.apply(this, arguments); }
    };

    var proto = new this(Class);
    var superClass = this.prototype;

    for (var n in def) {
        var item = def[n];

        if (item instanceof Function) {
            item = Class.__asMethod__(item, superClass);
        }

        proto[n] = item;
    }

    proto._$ = superClass;
    classDef.prototype = proto;

    //Give this new class the same static extend method
    classDef.extend = this.extend;
    return classDef;
};
