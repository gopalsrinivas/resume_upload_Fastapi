PGDMP      6                |            fastapi_resume_upload_aws    17.2    17.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16402    fastapi_resume_upload_aws    DATABASE     �   CREATE DATABASE fastapi_resume_upload_aws WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
 )   DROP DATABASE fastapi_resume_upload_aws;
                     gopal    false            �           0    0 "   DATABASE fastapi_resume_upload_aws    ACL     �   REVOKE ALL ON DATABASE fastapi_resume_upload_aws FROM gopal;
GRANT CREATE,CONNECT ON DATABASE fastapi_resume_upload_aws TO gopal;
GRANT TEMPORARY ON DATABASE fastapi_resume_upload_aws TO gopal WITH GRANT OPTION;
                        gopal    false    4861            �            1259    16403    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       gopal    false            �            1259    16409    careersusers    TABLE     t  CREATE TABLE public.careersusers (
    id integer NOT NULL,
    user_id character varying(50) NOT NULL,
    name character varying(150),
    email character varying(150),
    mobile character varying(150),
    is_active boolean,
    created_on timestamp without time zone NOT NULL,
    updated_on timestamp without time zone,
    resume_filename character varying(500)
);
     DROP TABLE public.careersusers;
       public         heap r       gopal    false            �            1259    16408    careersusers_id_seq    SEQUENCE     �   CREATE SEQUENCE public.careersusers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.careersusers_id_seq;
       public               gopal    false    219            �           0    0    careersusers_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.careersusers_id_seq OWNED BY public.careersusers.id;
          public               gopal    false    218            [           2604    16412    careersusers id    DEFAULT     r   ALTER TABLE ONLY public.careersusers ALTER COLUMN id SET DEFAULT nextval('public.careersusers_id_seq'::regclass);
 >   ALTER TABLE public.careersusers ALTER COLUMN id DROP DEFAULT;
       public               gopal    false    218    219    219            �          0    16403    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               gopal    false    217   �       �          0    16409    careersusers 
   TABLE DATA           |   COPY public.careersusers (id, user_id, name, email, mobile, is_active, created_on, updated_on, resume_filename) FROM stdin;
    public               gopal    false    219   �                   0    0    careersusers_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.careersusers_id_seq', 8, true);
          public               gopal    false    218            ]           2606    16407 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 gopal    false    217            _           2606    16416    careersusers careersusers_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.careersusers
    ADD CONSTRAINT careersusers_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.careersusers DROP CONSTRAINT careersusers_pkey;
       public                 gopal    false    219            a           2606    16418 %   careersusers careersusers_user_id_key 
   CONSTRAINT     c   ALTER TABLE ONLY public.careersusers
    ADD CONSTRAINT careersusers_user_id_key UNIQUE (user_id);
 O   ALTER TABLE ONLY public.careersusers DROP CONSTRAINT careersusers_user_id_key;
       public                 gopal    false    219            b           1259    16419    ix_careersusers_email    INDEX     V   CREATE UNIQUE INDEX ix_careersusers_email ON public.careersusers USING btree (email);
 )   DROP INDEX public.ix_careersusers_email;
       public                 gopal    false    219            c           1259    16420    ix_careersusers_mobile    INDEX     X   CREATE UNIQUE INDEX ix_careersusers_mobile ON public.careersusers USING btree (mobile);
 *   DROP INDEX public.ix_careersusers_mobile;
       public                 gopal    false    219            �      x�37M444J4HLN1����� *��      �   v  x����j�0���x����Iԣ]�;H6k[�S�`W?mvд
J@^B�����R�C?�6<���u�v^~<:wj�g߉�		�� �jH��4��KL����<	�,�`�+1g��n]S��m�2��m��,�BiI��W1TQ�N[�7�D��y�z��m��.PIFk/��8���.{?u�ih{W�?���~��R�O�1��u��r?~��.��7����d3
N��:��G�^�jU��&c0���b))�R��p/�u�)�Hes����a���A��T�&�bL�5*>PAJI�z�d����@�1�b*�Q鑊��b�&�bWm��O�+5�L���u��=O|E3�����NY�U�����p�2I�?ڊqi     