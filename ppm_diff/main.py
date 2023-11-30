
import imageio
filename = "10k_1_0000.ppm"
filename_ref = "10k_ref_1_0000.ppm"
img = imageio.imread(filename)
img_ref  = imageio.imread(filename_ref )

# for i in range(1024):
# 	for j in range(1024):
# 		for k in range(3):
# 			if diff[i][j][k] != 0:
# 				print(diff[i][j])
diff = abs(img_ref-img)
imageio.imwrite("diff.ppm", diff)
imageio.imwrite("show.ppm", img+10*diff)

