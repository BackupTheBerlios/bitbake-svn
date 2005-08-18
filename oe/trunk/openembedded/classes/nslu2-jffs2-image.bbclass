NSLU2_SLUGIMAGE_ARGS ?= ""

nslu2_pack_image () {
	install -d ${DEPLOY_DIR_IMAGE}/slug
	install -m 0644 ${STAGING_LIBDIR}/nslu2-binaries/RedBoot \
			${STAGING_LIBDIR}/nslu2-binaries/Trailer \
			${STAGING_LIBDIR}/nslu2-binaries/SysConf \
			${DEPLOY_DIR_IMAGE}/slug/
	install -m 0644 ${DEPLOY_DIR_IMAGE}/zImage-${IMAGE_BASENAME} ${DEPLOY_DIR_IMAGE}/slug/vmlinuz
	install -m 0644 ${DEPLOY_DIR_IMAGE}/${IMAGE_NAME}.rootfs.jffs2 ${DEPLOY_DIR_IMAGE}/slug/flashdisk.jffs2
	cd ${DEPLOY_DIR_IMAGE}/slug
	slugimage -p -b RedBoot -s SysConf -r Ramdisk:1,Flashdisk:flashdisk.jffs2 -t Trailer \
	  -o ${DEPLOY_DIR_IMAGE}/${IMAGE_NAME}.flashdisk.img ${NSLU2_SLUGIMAGE_ARGS}
	rm -rf ${DEPLOY_DIR_IMAGE}/slug
}

EXTRA_IMAGEDEPENDS += 'slugimage-native nslu2-linksys-firmware'
IMAGE_POSTPROCESS_COMMAND += "nslu2_pack_image; "
