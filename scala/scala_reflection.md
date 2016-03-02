# ���t���N�V����

## �Q�l

- Reflection - �T�v - Scala Documentation
  http://docs.scala-lang.org/ja/overviews/reflection/overview.html
- API document
  http://www.scala-lang.org/api/2.11.7/scala-reflect/#scala.reflect.package

## �T�v

���t���N�V�����łł��邱��

1. ���s�����t���N�V�����B
   ���s���Ƀ����^�C���^ (runtime type) �₻�̃����o���C���X�y�N�g������
   �Ăяo���\�́B
2. �R���p�C�������t���N�V�����B
   �R���p�C�����ɒ��ۍ\���؂ɃA�N�Z�X������A����𑀍삷��\�́B
3. ���C�t�B�P�[�V���� (reification)�B
   (1) �̏ꍇ�͎��s���ɁA(2) �̏ꍇ�̓R���p�C�����ɒ��ۍ\���؂𐶐����邱�ƁB


���s�����t���N�V�����łł��邱��

- ���̃I�u�W�F�N�g���ǂ̌^�����킩��
- �V�����I�u�W�F�N�g���쐬���邱�Ƃ��ł���
- ���̃I�u�W�F�N�g�̃����o�ɃA�N�Z�X������Ăяo������ł���


## ���j�o�[�X(Universe)

���s�����t���N�V�������A�R���p�C�������t���N�V��������I�ԁB
�ǂ���� universe �Ƃ��������C���^�[�t�F�[�X�ɒ��ۉ�����Ă���B

- ���s�����t���N�V�����̂��߂ɂ� `scala.reflect.runtime.universe`
- �R���p�C�������t���N�V�������߂ɂ� `scala.reflect.macros.Universe`


## ��{�v�f

- ���O(Name) : ���O��\������B������̔������b�p�[
- �V���{��(Symbol) : ���O�Ǝ��̂̃o�C���f�B���O�B�~���[����q�~���[�𓾂邽�߂Ɏg���B
- �^(Type): �V���{���̌^���
- �~���[(Mirror): �C���X�^���X�⃁�\�b�h���A���t���N�V�����I�ɑ��삷�邽�߂̌������������́B

### ���O (Name)

http://www.scala-lang.org/api/2.11.7/scala-reflect/#scala.reflect.api.Names

- TermName: �I�u�W�F�N�g�⃁���o�[(�t�B�[���h,���\�b�h�A�ϐ�)�̖��O
- TypeName: �N���X�A�g���C�g�A�^�����o�[(type�ŏ������)�̖��O

������@
```
TermName("map")
"map": TermName   // �����񃊃e��������̈Öق̌^�ϊ����g����
```

���\�b�h

- decodedName: b_=, <init>  �Ȃ�
- encodedName: b_$eq, $lessinit$greater  �Ȃ�
- isTermName, isTypeName
- toTermName, toTypeName
- toString


### �^(Type)

������@
```
import scala.reflect.runtime.universe._

// �^�L�q�H����typeOf�œ���
typeOf[List[Int]]
  // �� scala.reflect.runtime.universe.Type = scala.List[Int]

// �C���X�^���X���瓾��
// ( �^�p�����^��context binding �𗘗p���邱�Ƃ� T �����܂����Ɠ��� )
def getType[T: TypeTag](obj: T) = typeOf[T]
getType(List(1,2,3))
  // �� scala.reflect.runtime.universe.Type = List[Int]

// �W���^
// http://www.scala-lang.org/api/2.11.7/scala-reflect/#scala.reflect.api.StandardDefinitions$DefinitionsApi
val intTpe = definitions.Int    // �Ђ���Ƃ���� IntTpe ���H
�Ȃ�
```

���Z

```
// �T�u�^�C�v�֌W ( <:< )
class A
class B extends A
typeOf[A] <:< typeOf[B]  // false
typeOf[B] <:< typeOf[A]  // true
// c.f. weak_<:<

// �^�̓����� ( =:= ) (���I == �ł͂Ȃ��I)
def getType[T: TypeTag](obj: T) = typeOf[T]
class A
val a1 = new A; val a2 = new A
getType(a1) =:= getType(a2)   // true

getType(List(1,2,3)) =:= getType(List(1.0, 2.0, 3.0))   // false
getType(List(1,2,3)) =:= getType(List(9,8,7))           // true

// �����o�Ɛ錾�̏Ɖ�
t.member(name): Universe.Symbol    // ���O���w�肵�Ď擾
t.declaration(name): Universe.Symbol
t.members: Universe.MemberScope    // �S���擾�BTraverse�ł���B
t.declaraions: Universe.MemberScope

typeOf[List[_]].member("map": TermName)
typeOf[List[_]].member("Self": TypeName)
```

### �V���{��(Symbol)

http://www.scala-lang.org/api/2.11.7/scala-reflect/#scala.reflect.api.Symbols

�V���{���͊K�w�\���ɂȂ��Ă���B
(���\�b�h�̓N���X�ɏ��L����A�N���X�̓p�b�P�[�W�ɏ��L�����)

- TypeSymbol (�^�V���{��): �^�A�N���X�A�g���C�g�A�^�p�����[�^
  - ClassSymbol: �N���X��g���C�g
- TermSymbol (���V���{��): val, var, def, �I�u�W�F�N�g�̐錾�A�p�b�P�[�W��l�̃p�����^
  - MethodSymbol: def �̐錾
  - ModuleSymbol: �V���O���g���I�u�W�F�N�g�̐錾
- NoSymbol: owner ���Ȃ����Ƃ�\���Ƃ���f�t�H���g�l�Ɏg�p�����

���\�b�h

- (Symbol)
  - name, fullName
  - isConstructor
  - isAbstruct, isFinal, isJava, isPackage, 
  - isPrivate, isProtected, isPublic, 
  - isClass, isMethod, isModule, isModulueClass, isTerm, isType
  - companion
  - (TypeSymbol)
    - isAbstructType, isContravariant, isCovariant
    - (ClassSymbol)
      - isFinal, isPrivate, isProtected, isAbstractClass
      - baseClasses
      - typeParamas
    

������@

- Type �� member���\�b�h�� declaraion ���\�b�h

�V���{���ϊ�

member �́ASymbol �̃C���X�^���X��Ԃ��̂ŁA
����� MethodSymbol �ɕϊ�����K�v������B

- asClass, asMethod, asModule, asTerm, asType

```scala
import scala.reflect.runtime.{universe => ru}
class C[T] { def test[U](x: T)(y: U): Int = ??? }  // ���������N���X���������Ƃ���

val testMember = ru.typeOf[C[Int]].member(ru.TermName("test"))
  // �� scala.reflect.runtime.universe.Symbol = method test

testMember.asMethod
  // �� scala.reflect.runtime.universe.MethodSymbol = method test
```


### �~���[(Mirror)

�傫��2���
- �N���X���[�_�[�~���[: 
  (staticClass/staticModule/staticPackage ���\�b�h���g����) 
  ���O���V���{���ւƖ|�󂷂�B
- invoker�~��:
  (MethodMirror.apply �� FieldMirror.get �Ƃ��������\�b�h���g����)
  ���t���N�V������p�����Ăяo������������B

���s���~���[

- �N���X���[�_�[�~���[: (ReflectiveMirror�^)
- invoker�~���[:
  - InstanceMirror: �C���X�^���X�̃~���[
  - MethodMirror: �C���X�^���X�̃��\�b�h�̃~���[
  - FieldMirror: �C���X�^���X�̃t�B�[���h�̃~���[
  - ClassMirror: �N���X�̃~���[(�R���X�g���N�^�̃~���[���쐬����̂Ɏg��)
  - ModuleMirror: �V���O���g���I�u�W�F�N�g�̃~���[

������@

- �N���X���[�_�[�~���[�́A���ߑł��Ŏ擾
- ���ɂ���~���[����Areflect, reflectMethod, reflectField �Ȃǂ� Symbol ��n���ČĂԂ��ƂŁA
  Symbol �ɑΉ�����~���[��������B

�R���p�C�����~���[

�R���p�C�����~���[�͖��O����V���{����ǂݍ��ރN���X���[�_�~���[�������g����B
(���Ƃ܂킵)




## �T���v���R�[�h (���s��)

```
import scala.reflect.runtime.{universe => ru}

// �N���X���[�_�[�~���[�̎擾�B�قڂ���
val m = ru.runtimeMirror(getClass.getClassLoader)

// ����C���X�^���X�̃��\�b�h���Ăт����B
// class C { def x = 2 }     // ���������N���X���������Ƃ���
val im = m.reflect(new C)   // InstanceMirror �̎擾
val methodX = ru.typeOf[C].declaration(ru.TermName("x")).asMethod  // MethodSymbol �������
val mm = im.reflectMethod(methodX)   // method mirror �̎擾
mm()                                 // ���\�b�h�̎��s

// ����C���X�^���X�̃t�B�[���h�𑀍삵�����B
// class C { val x = 2; var y = 3 }  // ���������N���X���������Ƃ���
val im = m.reflect(new C)    // InstanceMirror �̎擾
val fieldX = ru.typeOf[C].declaration(ru.TermName("x")).asTerm.accessed.asTerm  // TermSymbol�������
val fmX = im.reflectField(fieldX)    // FieldMirror �̎擾
fmX.get
fmX.set(3)
```







==================================================
java �� ���t���N�V�����𗘗p�����Â�����
���[��B���܂��t�B�[���h�������Ȃ������肵�āA�悭�킩��Ȃ�...�B

�N���X�̎擾

val c = classOf[�N���X��]     // �N���X������
val c = obj.getClass()        // �C���X�^���X����
// java.lang.Class[T] �^
�� http://docs.oracle.com/javase/jp/8/docs/api/java/lang/Class.html


�����o�[�̎擾
c.CanonicalName  // �N���X��������B
c.GetName

c.getClasses()   // �����o�[�N���X�A�C���^�[�t�F�[�X�̎擾

c.getDeclaredFields()   // �S�Ẵt�B�[���h�BField[] �^
c.getFields()           // public �ȃt�B�[���h�BField[] �^

c.getDeclaredMethods()  // �S�Ẵ��\�b�h�B�p�����ꂽ���̂͊܂܂�Ȃ��B Method[] �^
c.getMethods()          // public �ȃ��\�b�h�B�p�����ꂽ���̊܂ށBMethod[] �^

Field�^
    f.getName()         // �t�B�[���h����Ԃ�

c.getFields.map(_.getName)
