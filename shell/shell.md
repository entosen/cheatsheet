�V�F���X�N���v�g

```
if [ ���� ] ; then
    ...
fi
```

test�R�}���h

    �t�@�C���n
    -e File   ���݂���� True


ls 
    -S     �t�@�C���T�C�Y�Ń\�[�g



pushd
popd
dirs
    -c  �N���A
    -v  �c�\��




wget

```
wget -nv -O - --save-headers 'http://entosen.tokyo:8080/status.html'
    -q    �G���[���������o���Ȃ�
    -nv   �G���[���ɂ͂�����o�͂���
    �Ȃ�  �i���o�[�̂悤�Ȃ��̂��o��

# POST
wget -nv -O - --save-headers --post-data 'data.......' 'http://entosen.tokyo:8080'
```

curl 

```
curl http://www.example.com/

    -s  �i���ƃG���[��\�����Ȃ�

    -i  ���X�|���X�w�b�_��\������
    -v  �ʐM�̂������ڍׂɕ\������

    �f�[�^�̎w��B�t�@�C�������w�肷��ꍇ�� @�t�@�C����
	--data <data>                 
	--data-binary <data>   
	--data-urlencode <data>   
```

