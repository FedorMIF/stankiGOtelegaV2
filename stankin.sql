PGDMP     "    .                {            stankin    15.2    15.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    82358    stankin    DATABASE     {   CREATE DATABASE stankin WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE stankin;
                postgres    false            �            1259    82393    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name text NOT NULL,
    role text NOT NULL,
    "group" text,
    role_group text,
    phone text,
    email text
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    82392    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    215                        0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    214            e           2604    82396    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    214    215    215            �          0    82393    users 
   TABLE DATA           [   COPY public.users (id, user_id, name, role, "group", role_group, phone, email) FROM stdin;
    public          postgres    false    215   �                  0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 8, true);
          public          postgres    false    214            g           2606    82400    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    215            i           2606    82402    users users_user_id_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_id_key UNIQUE (user_id);
 A   ALTER TABLE ONLY public.users DROP CONSTRAINT users_user_id_key;
       public            postgres    false    215            �   6  x���;N1���)�GA~���	�T)@�bţ �l
(( )BA��XB$�T��@N¬���5�gƞ���%k�$��J�#�.�c�>0ǻ��+�/���Skge"$�H�8�[p0wvg��.0A��p�����G�����mĿ�����g��2��U>��=ދ��H%��VGmgG���k�S)c�� ���r���=Ό�'�|�!G��a��9Wz�cL�=S�l�[��L�J�(����(k��#JHicd�jh�x� ;��֫TdL*�B�`O�#\1ߴ�{-���K='O����h�(h��֦�ĉ�     