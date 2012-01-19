#include "MyObj.hxx"

namespace foo {

// Returns the current env

JNIEnv * MyObj::getCurrentEnv() {
JNIEnv * curEnv = NULL;
jint res=this->jvm->AttachCurrentThread(reinterpret_cast<void **>(&curEnv), NULL);
if (res != JNI_OK) {
throw GiwsException::JniException(getCurrentEnv());
}
return curEnv;
}
// Destructor

MyObj::~MyObj() {
JNIEnv * curEnv = NULL;
this->jvm->AttachCurrentThread(reinterpret_cast<void **>(&curEnv), NULL);

curEnv->DeleteGlobalRef(this->instance);
curEnv->DeleteGlobalRef(this->instanceClass);
}
// Constructors
MyObj::MyObj(JavaVM * jvm_) {
jmethodID constructObject = NULL ;
jobject localInstance ;
jclass localClass ;
const std::string construct="<init>";
const std::string param="()V";
jvm=jvm_;

JNIEnv * curEnv = getCurrentEnv();

localClass = curEnv->FindClass( this->className().c_str() ) ;
if (localClass == NULL) {
  throw GiwsException::JniClassNotFoundException(curEnv, this->className());
}

this->instanceClass = static_cast<jclass>(curEnv->NewGlobalRef(localClass));

/* localClass is not needed anymore */
curEnv->DeleteLocalRef(localClass);

if (this->instanceClass == NULL) {
throw GiwsException::JniObjectCreationException(curEnv, this->className());
}


constructObject = curEnv->GetMethodID( this->instanceClass, construct.c_str() , param.c_str() ) ;
if(constructObject == NULL){
throw GiwsException::JniObjectCreationException(curEnv, this->className());
}

localInstance = curEnv->NewObject( this->instanceClass, constructObject ) ;
if(localInstance == NULL){
throw GiwsException::JniObjectCreationException(curEnv, this->className());
}
 
this->instance = curEnv->NewGlobalRef(localInstance) ;
if(this->instance == NULL){
throw GiwsException::JniObjectCreationException(curEnv, this->className());
}
/* localInstance not needed anymore */
curEnv->DeleteLocalRef(localInstance);

                /* Methods ID set to NULL */
voidbarjdoubleArray_doubleID=NULL;


}

MyObj::MyObj(JavaVM * jvm_, jobject JObj) {
        jvm=jvm_;

        JNIEnv * curEnv = getCurrentEnv();

jclass localClass = curEnv->GetObjectClass(JObj);
        this->instanceClass = static_cast<jclass>(curEnv->NewGlobalRef(localClass));
        curEnv->DeleteLocalRef(localClass);

        if (this->instanceClass == NULL) {
throw GiwsException::JniObjectCreationException(curEnv, this->className());
        }

        this->instance = curEnv->NewGlobalRef(JObj) ;
        if(this->instance == NULL){
throw GiwsException::JniObjectCreationException(curEnv, this->className());
        }
        /* Methods ID set to NULL */
        voidbarjdoubleArray_doubleID=NULL;


}

// Generic methods

void MyObj::synchronize() {
if (getCurrentEnv()->MonitorEnter(instance) != JNI_OK) {
throw GiwsException::JniMonitorException(getCurrentEnv(), "MyObj");
}
}

void MyObj::endSynchronize() {
if ( getCurrentEnv()->MonitorExit(instance) != JNI_OK) {
throw GiwsException::JniMonitorException(getCurrentEnv(), "MyObj");
}
}
// Method(s)

void MyObj::bar (JavaVM * jvm_, double* data, int dataSize){

JNIEnv * curEnv = NULL;
jvm_->AttachCurrentThread(reinterpret_cast<void **>(&curEnv), NULL);
jclass cls = curEnv->FindClass( className().c_str() );

jmethodID voidbarjdoubleArray_doubleID = curEnv->GetStaticMethodID(cls, "bar", "(Ljava/nio/DoubleBuffer;)V" ) ;
if (voidbarjdoubleArray_doubleID == NULL) {
throw GiwsException::JniMethodNotFoundException(curEnv, "bar");
}

//jdoubleArray data_ = curEnv->NewDoubleArray( dataSize ) ;
jobject buffer = curEnv->NewDirectByteBuffer((void*)data, (jlong)dataSize * sizeof(double));
if (!buffer)
{
    throw GiwsException::JniBadAllocException(curEnv);
}

// tu peux mettre en cache ByteOrderClass, nativeOrderID, bbCls et asdbID
// Les modifs ont essentiellement lieu ici
jclass ByteOrderClass = curEnv->FindClass("java/nio/ByteOrder");
if (ByteOrderClass == NULL) {
curEnv->ExceptionDescribe();
}
// public static ByteOrder nativeOrder()
jmethodID nativeOrderID = curEnv->GetStaticMethodID(ByteOrderClass, "nativeOrder", "()Ljava/nio/ByteOrder;");
if (nativeOrderID == NULL) {
curEnv->ExceptionDescribe();
}

//jmethodID nativeOrderID = curEnv->GetStaticMethodID(ByteOrderClass, "nativeOrder", "()Ljava/nio/ByteBuffer;");
jobject nativeOrder = curEnv->CallStaticObjectMethod(ByteOrderClass, nativeOrderID);//, buffer);

jclass bbCls = curEnv->FindClass("java/nio/ByteBuffer");
if (bbCls == NULL) {
curEnv->ExceptionDescribe();
}

jmethodID orderID = curEnv->GetMethodID(bbCls, "order", "(Ljava/nio/ByteOrder;)Ljava/nio/ByteBuffer;");
if (orderID == NULL) {
curEnv->ExceptionDescribe();

}

buffer = curEnv->CallObjectMethod(buffer, orderID, nativeOrder);

jmethodID asdbID = curEnv->GetMethodID(bbCls, "asDoubleBuffer", "()Ljava/nio/DoubleBuffer;");
if (asdbID == NULL) {
curEnv->ExceptionDescribe();

}

jobject dbuffer = curEnv->CallObjectMethod(buffer, asdbID);


if (dbuffer == NULL)
{
// check that allocation succeed
throw GiwsException::JniBadAllocException(curEnv);
}

curEnv->CallStaticVoidMethod(cls, voidbarjdoubleArray_doubleID, dbuffer);

// tu vires les refs ou autres

curEnv->DeleteLocalRef(cls);
if (curEnv->ExceptionCheck()) {
throw GiwsException::JniCallMethodException(curEnv);
}
}

}
